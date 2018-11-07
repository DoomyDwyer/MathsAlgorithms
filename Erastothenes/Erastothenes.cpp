// Erastothenes.cpp : Defines the entry point for the application.
//

#include "Erastothenes.h"
#include <vector>

using namespace std;

/*
 *
 * Input a number and use the Sieve of Erastothenes to display all prime numbers
 * between 2 and the entered number
 *
*/
int main()
{
	vector<bool>::size_type number;
	cout << "Sieve of Erastosthenes" << endl;
	cout << "Calculate primes between 2 and ";
	cin >> number;
	vector<bool> numbers(number + 1, true);

	//	cout << "Primes <= " + number << endl;
	for (decltype(numbers.size()) prime = 2; prime <= number; ++prime) {
		// TODO: Implement algorithm
		if (numbers[prime]) {
			cout << prime << endl;
		}
	}
	cout << endl << "Done." << endl;

	return 0;
}
