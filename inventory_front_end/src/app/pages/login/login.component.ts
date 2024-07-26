import { Component, inject, NgModule } from '@angular/core';
import { FormsModule, NgForm, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterLink, RouterOutlet } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-login',
  standalone: true,
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
  imports: [CommonModule, FormsModule]
})

export class LoginComponent {

  loginObj = {
    username: "",
    password: ""
  };

  constructor(private http: HttpClient, private router: Router) { }

  loginClick(): void {
    this.http.post('http://localhost:5000/api/login', this.loginObj).subscribe({
      next: (response: any) => {
        console.log('User logged in successfully', response);
        // localStorage.setItem('user-id', response.user.id);
        this.router.navigate(['/dashboard']);
      },
      error: (error) => {
        console.error('Error logging in', error);
        alert("Invalid username or pasword")
      }
    });
  }
}