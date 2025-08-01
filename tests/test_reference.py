import pytest, os, sys
from gis import reference as Reference

@pytest.mark.parametrize('shp_path',["./tests/datasets/series/georef-france-commune-millesime.shp"])
@pytest.mark.parametrize('version_id',["2012","2020"])
@pytest.mark.parametrize('key_expr',["code_com","dep_code+'_'+com_code"])
@pytest.mark.parametrize('defautvalue_expr',["com_name_lo","com_name_lo +' syn. '+ com_name_lo",])
def test_checkshpread(shp_path, version_id, key_expr, defautvalue_expr):
    Reference(shp_path, version_id, "k", key_expr, "dfv", defautvalue_expr)
    assert True