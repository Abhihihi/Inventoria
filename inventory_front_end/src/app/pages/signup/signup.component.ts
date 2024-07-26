import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.css',
  standalone: true,
  imports: [CommonModule, FormsModule]
})
export class SignupComponent {

  signupObj = {
    username: "",
    password: "",
    email: "",
  }

  constructor(private http: HttpClient) { }

  router = inject(Router)
  
  signupClick(): void {
    this.http.post("http://127.0.0.1:5000/api/register", this.signupObj).subscribe({
      next: (response) => {
        console.log('User registered successfully',response);
        this.router.navigateByUrl('login')
      },
      error: (error) => {
        console.error('Error registering user', error);
        alert("Invalid details")
      }
    });
    }
  }