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
    percentualMargin: string;
    price: string;
    post_discount_price: any[];
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

export const sendOrder = createAction('[Order] Send order.')
export const sendOrderSuccessfully = createAction('[Order] [Success] Send order.')
export const addOneToCart = createAction(
  '[App] Add one to cart.', props<{ payload : Product }>())
export const removeOneFromCart = createAction(
  '[App] Remove one from cart.', props<{ payload : Product }>())
export const getCart = createAction('[Cart] Get cart.')
export const setCart = createAction(
  '[Cart] Set cart.', props<{ payload : Cart }>())
export const setCartSuccessfully = createAction('[Cart] [Success] Set cart.')
export const setTotalOrderPrice = createAction(
  '[Order] Set totalOrderPrice.', props<{ payload : Cart["products"] }>())


export const appReducer = createReducer(
    appInitialState,
    on(addOneToCart, (state, { payload }) => {
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
            percentualMargin: payload.percentualMargin,  
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
    on(removeOneFromCart, (state, { payload }) => {
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
    on(setCart, (state, { payload }) => {
        state = {
            ...state,
            cart: payload
        }
        return state
    }),
    on(setTotalOrderPrice, (state, { payload }) => {
      let totalOrderPrice = 0
      console.log(payload)
      for (let product of payload) {
        if (product.units > 0) {
          totalOrderPrice += parseFloat(product.cost_price) * product.units
          for (let ingredient of product.ingredients){
            if (ingredient.qty > 0) {
              totalOrderPrice += (ingredient.price * ingredient.qty)
            }
          }
          totalOrderPrice *= parseFloat(product.percentualMargin)
        }
      }
      state = {
        ...state,
        totalOrderPrice: totalOrderPrice
      }
      return state
    })
)
