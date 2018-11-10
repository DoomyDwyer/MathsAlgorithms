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

	vector<bool>::size_type number;
	cin >> number;

	// Initialise N+1 bools in a vector:
	// We'll ignore elements 0 & 1, allowing us to index the vector using the actual numbers
	// we're working with (2..N)
	// bools are set to true initially as they're all potential primes until 'crossed out' (i.e. set to false)
	const vector<bool>::size_type LIST_LENGTH = number + 1;
	vector<bool> numbers(LIST_LENGTH, true);

	const decltype(numbers.size()) FIRST_PRIME = 2;
	const decltype(numbers.size()) SQRT_OF_N = sqrt(number);
	decltype(numbers.size()) count = 0;

	// Get performance stats
	const clock_t begin_time = clock();

	decltype(numbers.size()) prime = FIRST_PRIME;
	while (prime <= SQRT_OF_N) {
		if (numbers[prime]) {
			// Cross out all multiples of the prime numberas
			for (decltype(numbers.size()) multiple = prime * 2; multiple < LIST_LENGTH; multiple += prime) {
				if (numbers[multiple]) {
					numbers[multiple] = false;
				}
			}

			cout << prime << endl;
			++count;
		}
		++prime;
	}

	// All subsequent 'uncrossed-out' numbers are, by definition, primes, so print them
	while (prime < LIST_LENGTH) {
		if (numbers[prime]) {
			cout << prime << endl;
			++count;
		}
		++prime;
	}

	cout << endl << "There are " << count << " prime numbers between " << FIRST_PRIME << " and " << number << " ." << endl;
	std::cout << "Time taken: " << float(clock() - begin_time) << " msecs";

	return 0;
}
