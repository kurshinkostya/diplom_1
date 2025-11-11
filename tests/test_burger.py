import pytest

from unittest.mock import Mock
from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestBurger:

    """ Тест на установку булочек """
    def test_set_buns(self):
        burger = Burger()
        bun = Bun("White bun", 100.0)
        burger.set_buns(bun)
        assert burger.bun == bun
        assert burger.bun.get_price() == 100.0
        assert burger.bun.get_name() == "White bun"

    """ Тест на добавление ингредиента """
    def test_add_ingredient(self):
        burger = Burger()
        ingredient = Ingredient(INGREDIENT_TYPE_FILLING, "cutlet", 200.0)
        burger.add_ingredient(ingredient)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0].get_name() == "cutlet"

    """ Тест на удаление ингредиента """
    def test_remove_ingredient(self):
        burger = Burger()
        ingredient = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 50.0)
        burger.add_ingredient(ingredient)
        burger.remove_ingredient(0)
        assert burger.ingredients == []

    """ Тест на добавление ингредиента"""
    def test_move_ingredient(self):
        burger = Burger()
        i1 = Ingredient(INGREDIENT_TYPE_SAUCE, "sauce1", 20.0)
        i2 = Ingredient(INGREDIENT_TYPE_FILLING, "filling1", 30.0)
        burger.add_ingredient(i1)
        burger.add_ingredient(i2)
        burger.move_ingredient(0, 1)
        assert burger.ingredients[0] == i2
        assert burger.ingredients[1] == i1

    """ Тест на получение цены бургера"""
    def test_get_price_with_real_objects(self):
        burger = Burger()
        bun = Bun("Black bun", 100.0)
        burger.set_buns(bun)
        burger.add_ingredient(Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 50.0))
        burger.add_ingredient(Ingredient(INGREDIENT_TYPE_FILLING, "cutlet", 150.0))
        assert burger.get_price() == pytest.approx(100.0 * 2 + 50.0 + 150.0)

    """ Тест на получение чека """
    def test_get_receipt_with_real_objects(self):
        burger = Burger()
        bun = Bun("Red bun", 100.0)
        burger.set_buns(bun)
        burger.add_ingredient(Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 50.0))
        burger.add_ingredient(Ingredient(INGREDIENT_TYPE_FILLING, "cutlet", 150.0))

        expected_receipt = (
            "(==== Red bun ====)\n"
            "= sauce hot sauce =\n"
            "= filling cutlet =\n"
            "(==== Red bun ====)\n\n"
            "Price: 400.0"
        )
        assert burger.get_receipt() == expected_receipt


    # тесты с использованием моков для полной изоляции
    
    def test_get_price_with_mocks(self):
        burger = Burger()

        mock_bun = Mock()
        mock_bun.get_price.return_value = 120.0
        burger.set_buns(mock_bun)

        mock_ing1 = Mock()
        mock_ing1.get_price.return_value = 30.0
        mock_ing2 = Mock()
        mock_ing2.get_price.return_value = 50.0

        burger.add_ingredient(mock_ing1)
        burger.add_ingredient(mock_ing2)

        assert burger.get_price() == 320.0

    def test_get_receipt_with_mocks(self):
        burger = Burger()

        mock_bun = Mock()
        mock_bun.get_name.return_value = "Mock Bun"
        mock_bun.get_price.return_value = 100.0

        mock_ing = Mock()
        mock_ing.get_type.return_value = INGREDIENT_TYPE_SAUCE
        mock_ing.get_name.return_value = "Mock Sauce"
        mock_ing.get_price.return_value = 50.0

        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ing)

        expected = (
            "(==== Mock Bun ====)\n"
            "= sauce Mock Sauce =\n"
            "(==== Mock Bun ====)\n\n"
            "Price: 250.0"
        )
        assert burger.get_receipt() == expected

    def test_remove_ingredient_invalid_index(self):
        burger = Burger()
        with pytest.raises(IndexError):
            burger.remove_ingredient(0)

    def test_move_ingredient_invalid_index(self):
        burger = Burger()
        burger.add_ingredient(Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 10.0))
        with pytest.raises(IndexError):
            burger.move_ingredient(5, 0)
