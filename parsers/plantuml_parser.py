"""
PlantUML architecture parser.
Supports a controlled subset of PlantUML component diagram syntax.
"""
from __future__ import annotations
import re
from core.models import Architecture, Component, DataFlow
from core.exceptions import ParseError
from parsers.base_parser import BaseParser

# Map PlantUML keywords → component types
_TYPE_MAP = {
    "actor":      "user",
    "component":  "service",
    "database":   "database",
    "node":       "service",
    "cloud":      "external",
    "rectangle":  "service",
    "queue":      "queue",
    "collections":"service",
    "boundary":   "service",
    "control":    "service",
    "entity":     "external",
    "interface":  "service",
    "storage":    "storage",
    "usecase":    "service",
    "package":    "service",
    "frame":      "service",
}

# Arrow patterns  A -> B  /  A --> B  /  A <-> B
_ARROW_RE = re.compile(
    r'^\s*"?([^"<>\-\n]+?)"?\s+'
    r'(-+>|<-+>|<-+|\.+>|<\.+)\s*'
    r'"?([^":\n]+?)"?'
    r'(?:\s*:\s*(.+))?\s*$'
)

_COMPONENT_RE = re.compile(
    r'^\s*(' + '|'.join(_TYPE_MAP.keys()) + r')\s+"?([^"\n]+?)"?'
    r'(?:\s+as\s+(\w+))?\s*(?:\{.*\})?\s*$',
    re.IGNORECASE,
)

_AS_RE = re.compile(r'^\s*\[([^\]]+)\]\s+as\s+(\w+)', re.IGNORECASE)
_BRACKET_RE = re.compile(r'^\s*\[([^\]]+)\]')


class PlantUMLParser(BaseParser):
    def parse(self, content: str) -> Architecture:
        lines = content.splitlines()
        arch  = Architecture(name="PlantUML Architecture")

        aliases: dict[str, str] = {}   # alias → real name
        components: dict[str, Component] = {}

        for line in lines:
            stripped = line.strip()

            # Skip directives / comments
            if (stripped.startswith("@")
                    or stripped.startswith("'")
                    or stripped.startswith("skinparam")
                    or stripped.startswith("title")
                    or stripped.startswith("note")
                    or stripped == ""):
                if stripped.startswith("title"):
                    arch.name = stripped[5:].strip().strip('"')
                continue

            # [Alias] as name
            m = _AS_RE.match(stripped)
            if m:
                real, alias = m.group(1).strip(), m.group(2).strip()
                aliases[alias] = real
                if real not in components:
                    c = Component(name=real, type="service")
                    components[real] = c
                continue

            # keyword "Name" as alias
            m = _COMPONENT_RE.match(stripped)
            if m:
                kw, name, alias = m.group(1).lower(), m.group(2).strip(), m.group(3)
                ctype = _TYPE_MAP.get(kw, "service")
                internet = ctype == "external" or "customer" in name.lower() or "user" in name.lower()
                c = Component(
                    name=name,
                    type=ctype,
                    internet_facing=internet,
                    authentication=(ctype not in ("external", "user")),
                )
                components[name] = c
                if alias:
                    aliases[alias] = name
                continue

            # [ComponentName] shorthand
            m = _BRACKET_RE.match(stripped)
            if m:
                name = m.group(1).strip()
                if name not in components:
                    c = Component(name=name, type="service")
                    components[name] = c
                continue

            # Arrow  A -> B : label
            m = _ARROW_RE.match(stripped)
            if m:
                src_raw   = m.group(1).strip().strip('"')
                arrow     = m.group(2)
                dst_raw   = m.group(3).strip().strip('"')
                label     = (m.group(4) or "").strip()

                src = aliases.get(src_raw, src_raw)
                dst = aliases.get(dst_raw, dst_raw)

                # Auto-create components if not seen yet
                for nm in (src, dst):
                    if nm and nm not in components:
                        components[nm] = Component(name=nm, type="service")

                if src and dst:
                    proto  = _guess_protocol(label)
                    is_enc = proto in ("HTTPS", "TLS", "SSL", "WSS")
                    bidir  = "<" in arrow
                    df = DataFlow(
                        source      = src,
                        destination = dst,
                        protocol    = proto,
                        data        = label,
                        encrypted   = is_enc,
                        bidirectional=bidir,
                    )
                    arch.data_flows.append(df)
                continue

        arch.components = list(components.values())

        if not arch.components:
            raise ParseError(
                "No components could be parsed from the PlantUML input. "
                "Please check the syntax and use supported keywords: "
                + ", ".join(_TYPE_MAP.keys())
            )

        return arch


def _guess_protocol(label: str) -> str:
    label_lower = label.lower()
    if "https" in label_lower:
        return "HTTPS"
    if "http" in label_lower:
        return "HTTP"
    if "sql" in label_lower or "db" in label_lower or "query" in label_lower:
        return "SQL"
    if "amqp" in label_lower or "queue" in label_lower or "message" in label_lower:
        return "AMQP"
    if "grpc" in label_lower:
        return "gRPC"
    if "ws" in label_lower or "websocket" in label_lower:
        return "WSS"
    if "mqtt" in label_lower:
        return "MQTT"
    if "rest" in label_lower or "api" in label_lower:
        return "HTTPS"
    return "HTTPS"
