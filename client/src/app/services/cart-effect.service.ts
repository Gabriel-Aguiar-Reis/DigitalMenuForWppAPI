import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import {
  Cart,
  sendOrderSuccessfully,
  IAppState,
  setCart,
  setCartSuccessfully,
  sendOrder,
  addOneProductToCart,
  removeOneProductFromCart,
  addOneIngredientToCart,
  removeOneIngredientFromCart,
  setTotalOrderPrice,
  setTotalOrderPriceSuccessfully,
} from '../store/app.state';
import { map, of, switchMap, tap, withLatestFrom } from 'rxjs';
import { Store } from '@ngrx/store';
import { ProductService } from './product.service';

@Injectable({
  providedIn: 'root'
})


export class CartEffectService {
  
  constructor(
    private actions$: Actions,
    private http: HttpClient,
    private store: Store<{ app: IAppState, cart: Cart }>,
    private productService: ProductService,
    ) {}
  
  private apiUrl = 'http://localhost:8000/api'
   
  initCart = createEffect(
    () => this.actions$.pipe(
      ofType('[App] Initialize'), 
      switchMap(() => this.http.get<any>(`${this.apiUrl}/cart/view/`, { withCredentials: true })),
      tap(cart => this.store.dispatch(setCart({ payload: cart }))),
      map(() => setCartSuccessfully())
    )
  );
  addOneProductToCart = createEffect(
    () => this.actions$.pipe(
      ofType(addOneProductToCart),
      withLatestFrom(this.store.select('app').pipe(map(app => app.cart))),
      switchMap(([action]) => {
        const productId = action.payload.id;
        const unitsToAdd = 1;
        return this.productService.addToCart(productId, unitsToAdd).pipe(
          switchMap(() => {
            return this.http.get<any>(`${this.apiUrl}/cart/view/`, { withCredentials: true }).pipe(
              map(newCart => {
                this.store.dispatch(setCart({ payload: newCart }));
                return setCartSuccessfully();
              })
            );
          })
        );
      })
    )
  );
  removeOneProductFromCart = createEffect(
    () => this.actions$.pipe(
      ofType(removeOneProductFromCart),
      withLatestFrom(this.store.select('app').pipe(map(app => app.cart))),
      switchMap(([action]) => {
        const productId = action.payload.id;
        const unitsToRemove = 1;
        return this.productService.removeFromCart(productId, unitsToRemove).pipe(
          switchMap(() => {
            return this.http.get<any>(`${this.apiUrl}/cart/view/`, { withCredentials: true }).pipe(
              map(newCart => {
                this.store.dispatch(setCart({ payload: newCart }));
                return setCartSuccessfully();
              })
            );
          })
        )}
      )   
    )
  )
  addOneIngredientToCart = createEffect(
    () => this.actions$.pipe(
      ofType(addOneIngredientToCart),
      withLatestFrom(this.store.select('app').pipe(map(app => app.cart))),
      switchMap(([action]) => {
        const productId = action.payload.product.id;
        const ingredientId = action.payload.ingredient.id
        const qtyToAdd = 1;
        return this.productService.addOneIngredientToCart(productId, ingredientId, qtyToAdd).pipe(
          switchMap(() => {
            return this.http.get<any>(`${this.apiUrl}/cart/view/`, { withCredentials: true }).pipe(
              map(newCart => {
                this.store.dispatch(setCart({ payload: newCart }));
                return setCartSuccessfully();
              })
            )
          })
        )
        }
      )
    )
  )
  removeOneIngredientFromCart = createEffect(
    () => this.actions$.pipe(
    ofType(removeOneIngredientFromCart),
    withLatestFrom(this.store.select('app').pipe(map(app => app.cart))),
    switchMap(([action]) => {
      const productId = action.payload.product.id;
      const ingredientId = action.payload.ingredient.id
      const qtyToRemove = 1;
      return this.productService.removeOneIngredientFromCart(productId, ingredientId, qtyToRemove).pipe(
        switchMap(() => {
          return this.http.get<any>(`${this.apiUrl}/cart/view/`, { withCredentials: true }).pipe(
            map(newCart => {
              this.store.dispatch(setCart({ payload: newCart }));
              return setCartSuccessfully();
            })
          )
        })
      )
    })
    )
  )
  sendOrder = createEffect(
    () => this.actions$.pipe(
      ofType(sendOrder),
      withLatestFrom(this.store.select('app').pipe(map(app => app))),
      switchMap(([, app ]) => {
        const orderUrl = "https://api.whatsapp.com/send?phone=5512981696818&text=";
        let order = `*NOVO PEDIDO FRESQUINHO*\n`;
        let totalOrderPrice =app.totalOrderPrice
        for (let product of app.cart.products) {
          if (product.units > 0) {
            order += `${product.units} x ${product.name}\n`;
            for (let ingredient of product.ingredients){
              if (ingredient.qty > 0) {
                order += `  ${ingredient.qty} x ${ingredient.name}\n`;
              }
            }
          }
        }
        order += `*Valor Total:* R$ ${totalOrderPrice.toFixed(2)}`;
  
        const apiEndpoint = orderUrl + encodeURIComponent(order);
        return window.location.href = apiEndpoint
  
      }),
      map(() => sendOrderSuccessfully())
    )
  )
  getTotalOrderPrice = createEffect(
    () => this.actions$.pipe(
      ofType(
        addOneProductToCart,
        removeOneProductFromCart,
        addOneIngredientToCart,
        removeOneIngredientFromCart,
        setCart
      ),
      withLatestFrom(this.store.select('app').pipe(map(app => app.totalOrderPrice))),
      switchMap(([action]) => {
        return this.http.get<any>(`${this.apiUrl}/cart/calculate_total_order_price/`, { withCredentials: true }).pipe(
          map(totalOrderPrice => {
            this.store.dispatch(setTotalOrderPrice({ payload : totalOrderPrice.total_order_price }))
            return setTotalOrderPriceSuccessfully()
          })
        )
      })
    )
  )
}
