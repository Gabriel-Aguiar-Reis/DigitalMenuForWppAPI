import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ProductService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  addToCart(productId: string, unitsToAdd: number): Observable<any> {
    const url = `${this.apiUrl}/cart/products/${productId}/add/${unitsToAdd}/`;
    return this.http.patch<any>(
      url, { 
        "uuid": productId, 
        "units_added": unitsToAdd 
      }, { withCredentials: true })
  }
  removeFromCart(productId: string, unitsToRemove: number): Observable<any> {
    const url = `${this.apiUrl}/cart/products/${productId}/remove/${unitsToRemove}/`;
    return this.http.patch<any>(
      url, { 
        "uuid": productId, 
        "units_removed": unitsToRemove 
      }, { withCredentials: true });
  }
  addOneIngredientToCart(productId: string, ingredientId: string, qtyToAdd: number) {
    const url = `${this.apiUrl}/cart/products/${productId}/ingredients/${ingredientId}/add_qty/${qtyToAdd}/`
    return this.http.patch<any>(
      url, { 
        "uuid": productId, 
        "ingredient_uuid": ingredientId, 
        "qty_added": qtyToAdd 
      }, { withCredentials: true })
  }
  removeOneIngredientFromCart(productId: string, ingredientId: string, qtyToRemove: number) {
    const url = `${this.apiUrl}/cart/products/${productId}/ingredients/${ingredientId}/remove_qty/${qtyToRemove}/`
    return this.http.patch<any>(
      url, { 
        "uuid": productId, 
        "ingredient_uuid": ingredientId, 
        "qty_removed": qtyToRemove 
      }, { withCredentials: true })
  }
  getProduct(productId: string): Observable<any> {
    const url = `${this.apiUrl}/products/${productId}/`;
    return this.http.get<any>(url, { withCredentials: true });
  }
  getProducts(): Observable<any> {
    const url = `${this.apiUrl}/products/`;
    return this.http.get<any>(url,{ withCredentials: true })
  }
}