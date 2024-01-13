import { createAction, createReducer, on, props } from "@ngrx/store";


export interface Product {
    id: string;
    type: string;
    name: string;
    promotion: string;
    units: number;
    post_discount_price: any[];
}

export interface Cart {
    products: Product[];
}

export interface IAppState {
    cart: Cart;
}

export const appInitialState: IAppState = {
    cart: {products: []},

}

export const addOneToCart = createAction('[App] Add one to cart.', props<{ payload : Product }>())
export const removeOneFromCart = createAction('[App] Remove one from cart.')
export const getCart = createAction('[Cart] Get cart.')
export const setCart = createAction('[Cart] Set cart.', props<{ payload : Cart }>())
export const setCartSuccessfully = createAction('[Cart] [Success] Set cart.')


export const appReducer = createReducer(
    appInitialState,
    on(addOneToCart, (state, { payload }) => {
        // Verifica se o produto já está no carrinho.
        const existingProduct = state.cart.products.find(product => product.id === payload.id);
    
        if (existingProduct) {
          // Incrementa a propriedade 'units'.
          const updatedProducts = state.cart.products.map(product =>
            product.id === payload.id ? { ...product, units: product.units + 1 } : product
          );
    
          // Retorna um novo estado com os produtos atualizados.
          return {
            ...state,
            cart: { products: updatedProducts },
          };
        } else {
          // Adiciona o novo produto ao carrinho.
          const newProduct = {
            id: payload.id,
            type: payload.type,  // Preencha com o tipo correto.
            name: payload.name,  // Preencha com o nome correto.
            promotion: payload.promotion,  // Preencha com a promoção correta.
            units: 1,
            post_discount_price: payload.post_discount_price,  // Preencha conforme necessário.
          };
    
          // Retorna um novo estado com o novo produto no carrinho.
          return {
            ...state,
            cart: { products: [...state.cart.products, newProduct] },
          };
        }
      }),
    on(removeOneFromCart, (state) => {
        state = {
            ...state
        }
        return state
    }),
    on(setCart, (state, { payload }) => {
        state = {
            ...state,
            cart: payload
        }
        return state
    })
)
