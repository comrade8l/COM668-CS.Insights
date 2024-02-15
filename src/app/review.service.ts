// review.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ReviewService {
  private apiUrl = 'http://localhost:5000/api/v1.0/feedback';

  constructor(private http: HttpClient) {}

  getReviews(): Observable<any> {
    return this.http.get(this.apiUrl);
  }
}
