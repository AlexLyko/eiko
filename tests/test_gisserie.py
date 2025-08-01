import pytest, os, sys
from gis import gisserie as GisSerie

@pytest.mark.parametrize('shp_path',["./tests/datasets/series/georef-france-commune-millesime.shp"])
@pytest.mark.parametrize('key_expr',["code_com","dep_code+'_'+com_code"])
@pytest.mark.parametrize('defautvalue_expr',["com_name_lo","com_name_lo +' syn. '+ com_name_lo",])
def test_checkshpread(shp_path, key_expr, defautvalue_expr):
    GisSerie(shp_path, "k", key_expr, "dfv", defautvalue_expr)
    assert True