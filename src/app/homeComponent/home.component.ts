import { Component, OnInit } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';
import { InventoryService } from '../inventory.service'; // Update the path as per your file structure
import { ReviewService } from '../review.service'; // Update the path as per your file structure

@Component({
  selector: 'home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  reviews: any[] = []; // Initialize reviews as an empty array
  featuredSkins: any[] = [];

  constructor(
    public authService: AuthService,
    private inventoryService: InventoryService,
    private reviewService: ReviewService // Inject the ReviewService
  ) {}

  ngOnInit() {
    // Fetch featured skins
    this.inventoryService.getFeaturedSkins().subscribe(data => {
      this.featuredSkins = data;
    }, error => console.error('Error fetching skins:', error));

    // Fetch reviews
    this.reviewService.getReviews().subscribe(data => {
      this.reviews = data;
    }, error => console.error('Error fetching reviews:', error));
  }

  calculatePercentageIncrease(currentPrice: number, previousPrice: number): string {
    const increase = ((currentPrice - previousPrice) / previousPrice) * 100;
    return `${increase.toFixed(1)}%`;
  }
}
