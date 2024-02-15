import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class InventoryService {
  constructor(private http: HttpClient) {}

  getFeaturedSkins(): Observable<any> {
    // Replace '/api/v1.0/skins' with your actual Flask endpoint
    return this.http.get('http://localhost:5000/api/v1.0/skins/random/');
  }
}
