import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TypeService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  getType(typeId: string): Observable<any> {
    const url = `${this.apiUrl}/types/${typeId}/`
    return this.http.get(url, { withCredentials: true })
  }
}
