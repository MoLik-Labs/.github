"""Monthly editorial rotation. Keep picks curated, not ranked by popularity."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Feature:
    project: str
    track: str
    copy: str
    path: str
    accent: str


FEATURES = (
    Feature('Q-FOX-Algorithm', 'Algorithm notebook', 'Trace a cube-solving method from engine to results.', 'tree/main/results', '#cba6f7'),
    Feature('STUDY-SITE', 'Interface notebook', 'Read a study interface and its behavior in one HTML file.', '', '#f5c2e7'),
    Feature('ZMRIG', 'Systems notebook', 'Start at the Zig entry point for the RandomX miner.', 'blob/BETA/zmrig/src/main.zig', '#fab387'),
    Feature('MOLIK_WINLIK', 'Windows notebook', 'Explore the PowerShell side of Windows configuration.', '', '#94e2d5'),
)


def select(day):
    return FEATURES[(day.year * 12 + day.month - 1) % len(FEATURES)]
