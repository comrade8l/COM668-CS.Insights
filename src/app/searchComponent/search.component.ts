import { Component, OnInit } from '@angular/core';
import { WebService } from '../web.service';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';
import { Location } from '@angular/common';


@Component({
  selector: 'search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})

export class SearchComponent implements OnInit {
  business_list: any = [];

  constructor(public webService: WebService,
    private route: ActivatedRoute,
    private router: Router,
    private location: Location) {}

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      const searchTerm = params['term'];
      if (searchTerm) {
        this.business_list = this.webService.getSearchResults(searchTerm);
      }
    });
  }
  onSubmit(searchTerm: string) {
    // Handle the form submission
    // For example, you might call a service to fetch the search results
  }
}
