import { Component } from '@angular/core';
import { WebService } from '../web.service';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormControl, FormGroup, FormsModule, Validators } from '@angular/forms';
import { AuthService } from '@auth0/auth0-angular';
import { Injectable } from '@angular/core';
import { Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


@Component({
  selector: 'business',
  templateUrl: './business.component.html',
  styleUrls: ['./business.component.css']
})

@Injectable({
  providedIn: 'root'
})

export class BusinessComponent {
  business_list: any = [];
  reviews: any = [];
  reviewForm: any;
  LibraryAddForm: any;
  DeleteGameForm: any;
  username : any;
  businessId: any;



  constructor(private webService: WebService,
    private route: ActivatedRoute,
    private formBuilder: FormBuilder,
    private router: Router,
    private libraryFormBuilder: FormBuilder,
    @Inject(HttpClient) private http: HttpClient,
    public authService: AuthService) {}





  onSubmit() {
    this.webService.postReview(this.reviewForm.value)
      .subscribe((response: any) => {
        this.reviewForm.reset();
        this.reviews = this.webService.getReviews(this.route.snapshot.params['id']);
 });
    }

  addToLibrary(userEmail:any)  {
    this.username = userEmail
    this.createLibraryAddForm()
    this.webService.addToLibrary(this.LibraryAddForm.value)
    .subscribe((response: any) =>  {
      this.LibraryAddForm.reset();
    });
  }

  isInvalid(control: any) {
    return this.reviewForm.controls[control].invalid &&
    this.reviewForm.controls[control].touched;
    }

  isUntouched() {
    return this.reviewForm.controls.username.pristine ||
    this.reviewForm.controls.comment.pristine;
    }

  isIncomplete() {
  return this.isInvalid('username') ||
  this.isInvalid('comment') ||
  this.isUntouched();
  }

  createLibraryAddForm() {
    this.LibraryAddForm = this.libraryFormBuilder.group({
      bookmark: [this.username]
      });
  }

  ngOnInit() {
    this.reviewForm = this.formBuilder.group({
      username: ['', Validators.required],
      comment: ['', Validators.required],
      stars: 5
      });
    this.createLibraryAddForm()
    this.createDeleteGameForm();
    this.business_list = this.webService.getBusiness(this.route.snapshot.params['id']);
    this.reviews = this.webService.getReviews(this.route.snapshot.params['id'])
  }

createDeleteGameForm() {
  this.DeleteGameForm = this.formBuilder.group({
    id: [this.businessId]
  });
}


deleteGame() {
  this.businessId = this.route.snapshot.params['id'];
  this.createDeleteGameForm();
  this.webService.deleteGame(this.businessId)
    .subscribe(response => {
      this.router.navigate(['/businesses']);
    });
}



}
