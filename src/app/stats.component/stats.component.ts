import { Component } from '@angular/core';
import { WebService } from '../web.service';
import { ActivatedRoute } from '@angular/router'

@Component({
  selector: 'stats',
  templateUrl: './stats.component.html',
  styleUrls: ['./stats.component.css']
})

export class StatsComponent  {
  stats_list: any = [];
  page: number = 1;
  filters = { name: '',

};

  constructor(public webService: WebService, private route: ActivatedRoute) {}

  ngOnInit() {
    if (sessionStorage['page']) {
      this.page = Number(sessionStorage['page']);
      }
    this.stats_list = this.webService.getStats(this.page);
    }

    previousPage() {
      if (this.page > 1) {
        this.page = this.page - 1;
        sessionStorage['page'] = this.page;
        this.stats_list = this.webService.getStats(this.page);
        }
    }

    nextPage() {
      this.page = this.page + 1;
      sessionStorage['page'] = this.page;
      this.stats_list = this.webService.getStats(this.page);
    }

  }


