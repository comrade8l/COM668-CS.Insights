import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent } from './appComponent/app.component';
import { BusinessesComponent } from './businessesComponent/businesses.component';
import { BusinessComponent } from './businessComponent/business.component';
import { WebService } from './web.service';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { HomeComponent } from './homeComponent/home.component';
import { ReactiveFormsModule } from '@angular/forms';
import { AuthModule } from '@auth0/auth0-angular';
import { NavComponent } from './navComponent/nav.component';
import { LibraryComponent } from './libraryComponent/library.component';
import { SearchComponent } from './searchComponent/search.component';
import { ReviewsComponent } from './reviewsComponent/reviews.component';

var routes: any = [
    {
        path: '',
        component: HomeComponent
        },
        {
        path: 'businesses',
        component: BusinessesComponent
        },
        {
        path: 'businesses/:id',
        component: BusinessComponent
        },
        {
          path: 'library/:username',
          component: LibraryComponent
        },
        {
          path: 'search',
          component: SearchComponent
        },
        {
        path: 'reviews',
        component: ReviewsComponent
        },





];

@NgModule({
declarations: [
 AppComponent, BusinessesComponent, BusinessComponent, HomeComponent, NavComponent, LibraryComponent, SearchComponent
],
imports: [
 BrowserModule, HttpClientModule, RouterModule.forRoot(routes), ReactiveFormsModule,
 AuthModule.forRoot( {
    domain:'dev-6yi0u7n8pv4p7br5.us.auth0.com',
    clientId: 'NpVhH4qIUaf3iIYRR0zSwW3vahwDPnAs',
    authorizationParams: {
        redirect_uri: window.location.origin
      }
    })

],
providers: [WebService],
bootstrap: [AppComponent]
})
export class AppModule { }
