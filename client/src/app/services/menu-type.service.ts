import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MenuTypeService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  getTypes(): Observable<any> {
    const url = `${this.apiUrl}/types/`
    return this.http.get(url, { withCredentials: true })
  }
}
