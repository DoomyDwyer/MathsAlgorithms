// Erastothenes.cpp : The Sieve of Erastothenes .
//

#pragma once

#include <iostream>
#include <vector>
#include <ctime>

using namespace std;

/*
 *
 * Input a number and use the Sieve of Erastothenes to display all prime numbers
 * between 2 and the entered number
 *
*/
int main()
{
	cout << "Sieve of Erastothenes" << endl;
	cout << "Calculate primes between 2 and ";

	long long number;
	cin >> number;

	// Initialise N+1 bools in a dynamic array:
	// We'll ignore elements 0 & 1, allowing us to index the vector using the actual numbers
	// we're working with (2..N)
	// bools are set to true initially as they're all potential primes until 'crossed out' (i.e. set to false)
	const long long LIST_LENGTH = number + 1;

	cout << "Allocating memory... ";
	const clock_t alloc_begin_time = clock(); 
	bool *numbers = new bool [LIST_LENGTH];
	memset(numbers, true, LIST_LENGTH * sizeof(bool));
	cout << float(clock() - alloc_begin_time) << " msecs" << endl;

	const long long FIRST_PRIME = 2;
	const long long SQRT_OF_N = sqrt(number);
	//long long count = 0;

	// Get performance stats
	cout << "Running algorithm..." << endl;
	const clock_t begin_time = clock();

	long long prime = FIRST_PRIME;
	while (prime <= SQRT_OF_N) {
		if (numbers[prime]) {
			// Cross out all multiples of the prime numberas
			for (long long multiple = prime * 2; multiple < LIST_LENGTH; multiple += prime) {
				if (numbers[multiple]) {
					numbers[multiple] = false;
				}
			}

			//cout << prime << endl;
			//++count;
		}
		++prime;
	}

	// All subsequent 'uncrossed-out' numbers are, by definition, primes, so print them
	//while (prime < LIST_LENGTH) {
	//	if (numbers[prime]) {
	//		cout << prime << endl;
	//		++count;
	//	}
	//	++prime;
	//}

	//cout << endl << "There are " << count << " prime numbers between " << FIRST_PRIME << " and " << number << " ." << endl;
	std::cout << "Time taken: " << float(clock() - begin_time) << " msecs";

	delete[] numbers;
	return 0;
}
