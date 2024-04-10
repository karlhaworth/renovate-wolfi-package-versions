from pydantic import BaseModel


class Releases(BaseModel):
    version: str
    isDeprecated: bool | None = None
    releaseTimestamp: str | None = None
    changelogUrl: str | None = None
    sourceUrl: str | None = None
    sourceDirectory: str | None = None
    digest: str | None = None
    lts: bool | None = None


class Response(BaseModel):
    releases: list[Releases]
    sourceUrl: str | None = None
    sourceDirectory: str | None = None
    changelogUrl: str | None = None
    homepage: str | None = None
