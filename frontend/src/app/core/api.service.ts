import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
export interface Animal { id: number; name: string; species: string; sex: string; status: string; clinical_notes: string; allergies?: string; }
export interface StockItem { id: number; name: string; category: string; unit: string; quantity: number; minimum_quantity: number; expiration_date?: string; }
@Injectable({providedIn: 'root'}) export class ApiService {
  private http = inject(HttpClient); private token = '';
  private headers() { return { headers: new HttpHeaders({ Authorization: `Bearer ${this.token}` }) }; }
  login(email: string, password: string) { return this.http.post<{access_token: string}>('/api/auth/login', {email, password}); }
  setToken(token: string) { this.token = token; }
  getAnimals(): Observable<Animal[]> { return this.http.get<Animal[]>('/api/animals', this.headers()); }
  getStock(): Observable<StockItem[]> { return this.http.get<StockItem[]>('/api/stock', this.headers()); }
}
