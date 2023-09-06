from dataclasses import (
    dataclass,
    field,
)
from decimal import Decimal
from typing import (
    List,
    Optional,
)

from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "https://api.medunigraz.at/campusonline/linz/schema"


@dataclass
class GhkType:
    class Meta:
        name = "GHKType"

    titel: Optional[str] = field(
        default=None,
        metadata={
            "name": "TITEL",
            "type": "Attribute",
            "required": True,
        },
    )
    kurzbezeichnung: Optional[str] = field(
        default=None,
        metadata={
            "name": "KURZBEZEICHNUNG",
            "type": "Attribute",
            "required": True,
        },
    )
    credits: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CREDITS",
            "type": "Attribute",
        },
    )
    stp_lv_nr: Optional[int] = field(
        default=None,
        metadata={
            "name": "STP_LV_NR",
            "type": "Attribute",
            "required": True,
        },
    )
    nr: Optional[int] = field(
        default=None,
        metadata={
            "name": "NR",
            "type": "Attribute",
        },
    )
    sws: Optional[int] = field(
        default=None,
        metadata={
            "name": "SWS",
            "type": "Attribute",
        },
    )


@dataclass
class LvType:
    class Meta:
        name = "LVType"

    nr: Optional[int] = field(
        default=None,
        metadata={
            "name": "NR",
            "type": "Attribute",
            "required": True,
        },
    )
    ghk: Optional[int] = field(
        default=None,
        metadata={
            "name": "GHK",
            "type": "Attribute",
            "required": True,
        },
    )
    lvnr: Optional[str] = field(
        default=None,
        metadata={
            "name": "LVNR",
            "type": "Attribute",
        },
    )
    stoffsemester: Optional[str] = field(
        default=None,
        metadata={
            "name": "STOFFSEMESTER",
            "type": "Attribute",
        },
    )
    titel: Optional[str] = field(
        default=None,
        metadata={
            "name": "TITEL",
            "type": "Attribute",
        },
    )
    untertitel: Optional[str] = field(
        default=None,
        metadata={
            "name": "UNTERTITEL",
            "type": "Attribute",
        },
    )
    titel_engl: Optional[str] = field(
        default=None,
        metadata={
            "name": "TITEL_ENGL",
            "type": "Attribute",
        },
    )
    untertitel_eng: Optional[str] = field(
        default=None,
        metadata={
            "name": "UNTERTITEL_ENG",
            "type": "Attribute",
        },
    )
    lv_art: Optional[str] = field(
        default=None,
        metadata={
            "name": "LV_ART",
            "type": "Attribute",
        },
    )
    sws: Optional[int] = field(
        default=None,
        metadata={
            "name": "SWS",
            "type": "Attribute",
        },
    )
    credits: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CREDITS",
            "type": "Attribute",
        },
    )


@dataclass
class PvType:
    class Meta:
        name = "PVType"

    nr: Optional[int] = field(
        default=None,
        metadata={
            "name": "NR",
            "type": "Attribute",
        },
    )
    lv_nr: Optional[int] = field(
        default=None,
        metadata={
            "name": "LV_NR",
            "type": "Attribute",
            "required": True,
        },
    )
    datum_der_letztbeurteilung: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DATUM_DER_LETZTBEURTEILUNG",
            "type": "Attribute",
            "format": "%Y-%m-%dT%H:%M:%S",
        },
    )
    note: Optional[str] = field(
        default=None,
        metadata={
            "name": "NOTE",
            "type": "Attribute",
        },
    )
    prf_versuch: Optional[int] = field(
        default=None,
        metadata={
            "name": "PRF_VERSUCH",
            "type": "Attribute",
        },
    )
    titel: Optional[str] = field(
        default=None,
        metadata={
            "name": "TITEL",
            "type": "Attribute",
        },
    )
    pruefer_vorname: Optional[str] = field(
        default=None,
        metadata={
            "name": "PRUEFER_VORNAME",
            "type": "Attribute",
        },
    )
    pruefer_nachname: Optional[str] = field(
        default=None,
        metadata={
            "name": "PRUEFER_NACHNAME",
            "type": "Attribute",
        },
    )
    geschlecht: Optional[str] = field(
        default=None,
        metadata={
            "name": "GESCHLECHT",
            "type": "Attribute",
        },
    )
    matrikelnummer: Optional[int] = field(
        default=None,
        metadata={
            "name": "MATRIKELNUMMER",
            "type": "Attribute",
        },
    )
    skz: Optional[str] = field(
        default=None,
        metadata={
            "name": "SKZ",
            "type": "Attribute",
        },
    )
    studienplanversion: Optional[str] = field(
        default=None,
        metadata={
            "name": "STUDIENPLANVERSION",
            "type": "Attribute",
        },
    )
    anerkennung_ja_nein: Optional[str] = field(
        default=None,
        metadata={
            "name": "ANERKENNUNG_JA_NEIN",
            "type": "Attribute",
        },
    )
    anerkennungstitel_dt: Optional[str] = field(
        default=None,
        metadata={
            "name": "ANERKENNUNGSTITEL_DT",
            "type": "Attribute",
        },
    )
    anerkennungstitel_engl: Optional[str] = field(
        default=None,
        metadata={
            "name": "ANERKENNUNGSTITEL_ENGL",
            "type": "Attribute",
        },
    )
    anerkennungs_ects: Optional[int] = field(
        default=None,
        metadata={
            "name": "ANERKENNUNGS_ECTS",
            "type": "Attribute",
        },
    )
    anerkennungs_ghk: Optional[int] = field(
        default=None,
        metadata={
            "name": "ANERKENNUNGS_GHK",
            "type": "Attribute",
        },
    )


@dataclass
class FachType:
    class Meta:
        name = "FACHType"

    ghk: List[GhkType] = field(
        default_factory=list,
        metadata={
            "name": "GHK",
            "type": "Element",
            "namespace": __NAMESPACE__,
        },
    )
    credits: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CREDITS",
            "type": "Attribute",
        },
    )
    sws: Optional[int] = field(
        default=None,
        metadata={
            "name": "SWS",
            "type": "Attribute",
        },
    )
    kennung: Optional[str] = field(
        default=None,
        metadata={
            "name": "KENNUNG",
            "type": "Attribute",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Attribute",
        },
    )
    name_engl: Optional[str] = field(
        default=None,
        metadata={
            "name": "NAME_ENGL",
            "type": "Attribute",
        },
    )


@dataclass
class StplType:
    class Meta:
        name = "STPLType"

    fach: List[FachType] = field(
        default_factory=list,
        metadata={
            "name": "FACH",
            "type": "Element",
            "namespace": __NAMESPACE__,
            "min_occurs": 1,
        },
    )
    skz_uni: Optional[str] = field(
        default=None,
        metadata={
            "name": "SKZ_UNI",
            "type": "Attribute",
        },
    )
    skz_key: Optional[str] = field(
        default=None,
        metadata={
            "name": "SKZ_KEY",
            "type": "Attribute",
        },
    )
    skzkey_attribute: Optional[int] = field(
        default=None,
        metadata={
            "name": "SKZKEY",
            "type": "Attribute",
        },
    )
    skzbez: Optional[str] = field(
        default=None,
        metadata={
            "name": "SKZBEZ",
            "type": "Attribute",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "name": "VERSION",
            "type": "Attribute",
        },
    )
    gueltig_ab: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "GUELTIG_AB",
            "type": "Attribute",
            "format": "%Y-%m-%dT%H:%M:%S",
        },
    )
    gueltig_bis: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "GUELTIG_BIS",
            "type": "Attribute",
            "format": "%Y-%m-%dT%H:%M:%S",
        },
    )
    studierbar_bis: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "STUDIERBAR_BIS",
            "type": "Attribute",
            "format": "%Y-%m-%dT%H:%M:%S",
        },
    )
    abschnitt: Optional[int] = field(
        default=None,
        metadata={
            "name": "ABSCHNITT",
            "type": "Attribute",
        },
    )
    semester: Optional[int] = field(
        default=None,
        metadata={
            "name": "SEMESTER",
            "type": "Attribute",
        },
    )
    sws: Optional[int] = field(
        default=None,
        metadata={
            "name": "SWS",
            "type": "Attribute",
        },
    )
    credits: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CREDITS",
            "type": "Attribute",
        },
    )


@dataclass
class ExchangeType:
    class Meta:
        name = "EXCHANGEType"

    stpl: List[StplType] = field(
        default_factory=list,
        metadata={
            "name": "STPL",
            "type": "Element",
            "namespace": __NAMESPACE__,
        },
    )
    lv: List[LvType] = field(
        default_factory=list,
        metadata={
            "name": "LV",
            "type": "Element",
            "namespace": __NAMESPACE__,
        },
    )
    pv: List[PvType] = field(
        default_factory=list,
        metadata={
            "name": "PV",
            "type": "Element",
            "namespace": __NAMESPACE__,
        },
    )


@dataclass
class Exchange(ExchangeType):
    class Meta:
        name = "EXCHANGE"
        namespace = __NAMESPACE__
