import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ProductService {
  // private apiUrl = 'http://localhost:8000/api/products';

  // constructor(private http: HttpClient) {}

  // updateUnitsPurchased(productId: string, unitsPurchased: number): Observable<any> {
  //   const url = `${this.apiUrl}/${productId}/update_units_purchased`;
  //   return this.http.post(url, { "uuid": productId, "units_purchased": unitsPurchased }, { withCredentials: true });
  // }
}