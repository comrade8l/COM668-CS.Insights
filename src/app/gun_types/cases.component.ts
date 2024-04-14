import { Component } from '@angular/core';
import { WebService } from '../web.service';
import { ActivatedRoute } from '@angular/router'

@Component({
  selector: 'cases',
  templateUrl: './cases.component.html',
  styleUrls: ['./cases.component.css']
})

export class CasesComponent  {
  cases_list: any = [];
  page: number = 1;
  filters = { name: '',

};

  constructor(public webService: WebService, private route: ActivatedRoute) {}

  ngOnInit() {
    if (sessionStorage['page']) {
      this.page = Number(sessionStorage['page']);
      }
    this.cases_list = this.webService.getCasesSkins(this.page);
    }

    previousPage() {
      if (this.page > 1) {
        this.page = this.page - 1;
        sessionStorage['page'] = this.page;
        this.cases_list = this.webService.getCasesSkins(this.page);
        }
    }

    nextPage() {
      this.page = this.page + 1;
      sessionStorage['page'] = this.page;
      this.cases_list = this.webService.getCasesSkins(this.page);
    }

  }


