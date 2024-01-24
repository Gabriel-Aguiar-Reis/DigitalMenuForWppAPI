import { createAction, createReducer, on, props } from "@ngrx/store";

export interface Ingredient {
  id: string,
  name: string,
  qty: number,
  price: number
}

export interface Product {
    id: string;
    type: string;
    name: string;
    promotion: string;
    units: number;
    ingredients: Ingredient[];
    cost_price: string;
    percentual_margin: string;
    price: number;
    post_discount_price: any;
}

export interface Cart {
    products: Product[];
}

export interface IAppState {
    cart: Cart;
    isOrderGenerated: boolean
    totalOrderPrice: number
}

export const appInitialState: IAppState = {
    cart: {products: []},
    isOrderGenerated: false,
    totalOrderPrice: 0
}

export const sendOrder = createAction(
  '[Order] Send order')
export const sendOrderSuccessfully = createAction(
  '[Order] [Success] Send order')


export const addOneProductToCart = createAction(
  '[App] Add one product to cart', props<{ payload : Product }>())
export const removeOneProductFromCart = createAction(
  '[App] Remove one product from cart', props<{ payload : Product }>())

export const addOneIngredientToCart = createAction(
  '[App] Add one ingredient to cart', props<{ payload: { product: Product, ingredient: Ingredient } }>())
export const removeOneIngredientFromCart = createAction(
  '[App] Remove one ingredient from cart', props<{ payload: { product: Product, ingredient: Ingredient } }>())

export const initApp = createAction(
  '[App] Initialize')

export const setCart = createAction(
  '[Cart] Set cart', props<{ payload : Cart }>())
export const setCartSuccessfully = createAction(
  '[Cart] [Success] Set cart')

export const setTotalOrderPrice = createAction(
  '[Order] Set totalOrderPrice', props<{ payload : number}>()
)
export const setTotalOrderPriceSuccessfully = createAction(
  '[Order] [Successfully] Set totalOrderPrice')

export const appReducer = createReducer(
    appInitialState,
    on(addOneProductToCart, (state, { payload }) => {
        const existingProduct = state.cart.products.find(product => product.id === payload.id);
    
        if (existingProduct) {
          const updatedProducts = state.cart.products.map(product =>
            product.id === payload.id ? { ...product, units: product.units + 1 } : product
          );
    
          return {
            ...state,
            cart: { products: updatedProducts },
          };
        } else {
          const newProduct = {
            id: payload.id,
            type: payload.type,  
            name: payload.name,
            percentual_margin: payload.percentual_margin,  
            promotion: payload.promotion,  
            units: 1,
            price: payload.price,
            ingredients: payload.ingredients,
            cost_price: payload.cost_price,
            post_discount_price: payload.post_discount_price
          };
    
          return {
            ...state,
            cart: { products: [...state.cart.products, newProduct] },
          };
        }
      }),
    on(removeOneProductFromCart, (state, { payload }) => {
      const existingProduct = state.cart.products.find(product => product.id === payload.id);
    
      if (existingProduct) {
        const updatedProducts = state.cart.products.map(product =>
          product.id === payload.id ? { ...product, units: product.units - 1 } : product
        );
        return {
          ...state,
          cart: { products: updatedProducts },
        };
      }
      else { 
        return {
        ...state
        }
      }
      }),
    on(addOneIngredientToCart, (state, { payload }) => {
      const productId = payload.product.id;
      const ingredientId = payload.ingredient.id;
  
      const existingProduct = state.cart.products.find(product => product.id === productId);
  
      if (existingProduct) {
        const updatedProducts = state.cart.products.map(product => {
          if (product.id === productId) {
            const existingIngredient = product.ingredients.find(ingredient => ingredient.id === ingredientId);
  
            if (existingIngredient) {
              const updatedIngredients = product.ingredients.map(ingredient =>
                ingredient.id === ingredientId
                  ? { ...ingredient, qty: ingredient.qty + 1 }
                  : ingredient
              );
  
              return { ...product, ingredients: updatedIngredients };
            } else {
              const newIngredient: Ingredient = {
                id: ingredientId,
                name: payload.ingredient.name,
                qty: 1,
                price: payload.ingredient.price
              };
  
              return { ...product, ingredients: [...product.ingredients, newIngredient] };
            }
          } else {
            return product;
          }
        });
  
        return { ...state, cart: { products: updatedProducts } };
      } else {
        const newProduct: Product = {
          id: productId,
          type: payload.product.type,
          name: payload.product.name,
          percentual_margin: payload.product.percentual_margin,
          promotion: payload.product.promotion,
          units: 1,
          price: payload.product.price,
          ingredients: [
            {
              id: ingredientId,
              name: payload.ingredient.name,
              qty: 1,
              price: payload.ingredient.price
            }
          ],
          cost_price: payload.product.cost_price,
          post_discount_price: payload.product.post_discount_price
        };
  
        return { ...state, cart: { products: [...state.cart.products, newProduct] } };
      }
    }),
    on(removeOneIngredientFromCart, (state, { payload }) => {
      const productId = payload.product.id;
      const ingredientId = payload.ingredient.id;
  
      const existingProduct = state.cart.products.find(product => product.id === productId);
  
      if (existingProduct) {
        const updatedProducts = state.cart.products.map(product => {
          if (product.id === productId) {
            const existingIngredient = product.ingredients.find(ingredient => ingredient.id === ingredientId);
  
            if (existingIngredient) {
              const updatedIngredients = product.ingredients.map(ingredient =>
                ingredient.id === ingredientId
                  ? { ...ingredient, qty: ingredient.qty - 1 }
                  : ingredient
              ).filter(ingredient => ingredient.qty > 0);
  
              return { ...product, ingredients: updatedIngredients };
            } else {
              return product;
            }
          } else {
            return product;
          }
        })
        return { ...state, cart: { products: updatedProducts } };
      } else {
        return state;
      }
    }),
    on(setCart, (state, { payload }) => {
        state = {
            ...state,
            cart: payload
        }
        return state
    }),
    on(setTotalOrderPrice, (state, { payload }) => {
      return { ...state, totalOrderPrice: payload };
    })
)

