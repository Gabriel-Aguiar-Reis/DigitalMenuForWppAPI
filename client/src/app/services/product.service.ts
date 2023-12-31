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
    const url = `${this.apiUrl}/products/${productId}/add/${unitsToAdd}/`;
    return this.http.patch<any>(url, { "uuid": productId, "units_added": unitsToAdd }, { withCredentials: true });
  }
  removeFromCart(productId: string, unitsToAdd: number): Observable<any> {
    const url = `${this.apiUrl}/products/${productId}/remove/${unitsToAdd}/`;
    return this.http.patch<any>(url, { "uuid": productId, "units_removed": unitsToAdd }, { withCredentials: true });
  }
  getProduct(productId: string): Observable<any> {
    const url = `${this.apiUrl}/products/${productId}/`;
    return this.http.get<any>(url, { withCredentials: true });
  }
}