// reviews.component.ts
import { Component, OnInit } from '@angular/core';
import { ReviewService } from '../review.service';

@Component({
  selector: 'reviews',
  templateUrl: './reviews.component.html',
  styleUrls: ['./reviews.component.css']
})
export class ReviewsComponent implements OnInit {
  reviews: any[] = [];

  constructor(private reviewService: ReviewService) { }

  ngOnInit(): void {
    this.fetchReviews();
  }

  fetchReviews(): void {
    this.reviewService.getReviews().subscribe((data: any) => {
      this.reviews = data;
    });
  }
}
