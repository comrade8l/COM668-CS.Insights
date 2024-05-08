import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent } from './appComponent/app.component';
import { InspectComponent } from './inspectComponent/inspect.component';
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
import { ContentComponent } from './contentComponent/content.component';
import { PistolComponent } from './gun_types/pistol.component';
import { rifleComponent } from './gun_types/rifle.component';
import { SMGComponent } from './gun_types/smg.component';
import { HeavyComponent } from './gun_types/heavy.component';
import { CasesComponent } from './gun_types/cases.component';
import { StickerComponent } from './gun_types/sticker.component';
import { ListingsComponent } from './listings.component/listings.component';
import { StatsComponent } from './stats.component/stats.component';
import { SkinsComponent } from './skinsComponent/skins.component';



var routes: any = [
    {
        path: '',
        component: HomeComponent
        },
        {
        path: 'skins',
        component: SkinsComponent
        },
        {
        path: 'skins/:id',
        component: InspectComponent
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
        {
        path: 'content',
        component: ContentComponent
        },
        {
        path: 'pistol',
        component: PistolComponent
        },
        {
          path: 'rifle',
          component: rifleComponent
        },
        {
          path: 'smg',
          component: SMGComponent
        },
        {
          path: 'heavy',
          component: HeavyComponent
        },
        {
          path: 'cases',
          component: CasesComponent
        },
        {
          path: 'stickers',
          component: StickerComponent
        },
        {
          path: 'reviews',
          component: ReviewsComponent
        },
        {
          path: 'listing',
          component: ListingsComponent
        },
        {
          path: 'stats',
          component: StatsComponent
        },

];

@NgModule({
declarations: [
 AppComponent, SkinsComponent, InspectComponent, HomeComponent, NavComponent, LibraryComponent, SearchComponent, ReviewsComponent, ContentComponent, PistolComponent, rifleComponent, SMGComponent, HeavyComponent, CasesComponent, StickerComponent, ReviewsComponent, ListingsComponent, StatsComponent
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
