import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root' // Ensure this service is provided in the root module
})
export class WebService {

  private businessID: string | undefined; // It's good practice to specify types

  constructor(private http: HttpClient) {}

  getLibrary(username: string): Observable<any> {
    return this.http.get(`http://localhost:5000/api/v1.0/skins/bookmarks/${username}`);
  }

  getBusinesses(page: number): Observable<any> {
    return this.http.get(`http://localhost:5000/api/v1.0/skins?pn=${page}`);
  }
  //new stuff for filtering and sorting
  getPistolSkins(page: number): Observable<any> {
    // var sortValue
    // if (order === 1){
    //   sortValue = "ASC"
    // } else {
    //   sortValue = "DESC"
    // }
    return this.http.get(`http://localhost:5000/api/v2.0/skins/pistols?pn=${page}`);
  }

  getRifleSkins(page: number): Observable<any> {
    return this.http.get('http://localhost:5000/api/v2.0/skins/rifles?pn=1');
  }

  getSmgSkins(page: number): Observable<any> {
    return this.http.get('http://localhost:5000/api/v2.0/skins/smg?pn=1');
  }

  getHeavySkins(page: number): Observable<any> {
    return this.http.get('http://localhost:5000/api/v2.0/skins/heavy?pn=1');
  }
  
  getStickerSkins(page: number): Observable<any> {
    return this.http.get('http://localhost:5000/api/v2.0/skins/stickers?pn=1');
  }

  getCasesSkins(page: number): Observable<any> {
    return this.http.get('http://localhost:5000/api/v2.0/skins/containers?pn=1');
  }

  getBusiness(id: string): Observable<any> {
    this.businessID = id;
    return this.http.get(`http://localhost:5000/api/v1.0/skins/${id}`);
  }

  getReviews(id: string): Observable<any> {
    return this.http.get(`http://localhost:5000/api/v1.0/skins/${id}/reviews`);
  }

  getFloats(id: string): Observable<any> {
    return this.http.get(`http://localhost:5000/api/v1.0/skins/float?pn=1`);
  }
  getStats(page: number): Observable<any> {
    return this.http.get(`http://localhost:5000/api/v2.0/stats?pn=${page}`);
  }
  

  postReview(review: any): Observable<any> {
    let postData = new FormData();
    postData.append("username", review.username);
    postData.append("comment", review.comment);
    postData.append("stars", review.stars);

    let today = new Date();
    let todayDate = `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`;
    postData.append("date", todayDate);

    return this.http.post(`http://localhost:5000/api/v1.0/skins/${this.businessID}/reviews`, postData);
  }

  addToLibrary(user: any): Observable<any> {
    let putData = new FormData();
    putData.append("bookmark", user.bookmark);
    return this.http.put(`http://localhost:5000/api/v1.0/skins/update/bookmarks/${this.businessID}`, putData);
  }

  getSearchResults(searchTerm: string): Observable<any> {
    return this.http.get(`http://localhost:5000/api/v1.0/skins/search?name=${searchTerm}`);
  }

  deleteGame(businessID: string): Observable<any> {
    this.businessID = businessID;
    return this.http.delete(`http://localhost:5000/api/v1.0/skins/delete/${this.businessID}`);
  }

  // Optionally, if you also want to fetch price data as JSON
  getSkinPrice(id: string): Observable<any> {
    return this.http.get(`http://localhost:5000/api/v1.0/skins/price/${id}`);
  }
}
