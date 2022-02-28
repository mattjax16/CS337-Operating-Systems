 
//////////////////////////////////////////////////////////////////////
/// 
///             Software Development Laboratory <SDML> 
/// 
///                   Kent State University 
/// 
/// 
///   @file   : bigint.cpp
///   Author  : J. Maletic
///   Creation Date    : 8/16/2002
///   Purpose : Implementation of methods for class
///   Updated: Aug 2017
/// 
/// 
//////////////////////////////////////////////////////////////////////
/// 
//////////////////////////////////////////////////////////////////////
 
#include "bigint.hpp"


//////////////////////////////////////////////////////////////////////
/// PRE:  '0' <= ch <= '9'
/// POST: 0 .. 9
/// 
///
inline int digit_to_int(char ch) { return int(ch) - int('0'); }




 
//////////////////////////////////////////////////////////////////////
/// PRE:  <none>
/// POST: digit[0]...digit[CAPACTIY-1] == 0
/// 
bigint::bigint() {
    for (int i=0; i<CAPACTIY; ++i) digit[i] = 0;
    
    /// ASSERT: digit[0]...digit[CAPACTIY-1] == 0
    ///
}


//////////////////////////////////////////////////////////////////////
/// PRE:  num >= 0
/// Post:
///  num == 345 &&
///  a.digit[CAPACITY-1 .. 3] == 0 &&
///  a.digit[2] == 3 && a.digit[1] == 4 && a.digit[0] == 5
///
///
bigint::bigint(int num) : bigint() {
    int i = 0;
    while (num != 0) {
        digit[i] = num % 10;
        num = num / 10;
        i++;
    }
}

//////////////////////////////////////////////////////////////////////
/// PRE:  num must be a string of digits
/// POST: digit[n]==num[0] || digit[n-1]==num[1] ||...|| digit[0] == num[n]
/// 
bigint::bigint(const char num[])  : bigint() {
    int len = 0;
    while (num[len] != 0) ++len;

    for (int i = 0; i<len; ++i)
        digit[i] = digit_to_int(num[len-i-1]);
}

//////////////////////////////////////////////////////////////////////
/// PRE:  <none>
/// POST: RETVAL == the number of digits in the object.
/// 
int bigint::numberOfDigits () const {
    int n = CAPACTIY-1;
    while ((digit[n] == 0) && (n >= 0)) --n;
    
    return n+1;
}

//////////////////////////////////////////////////////////////////////
/// PRE:  <none>
/// POST: RETVAL == digit at 10^i
/// 
int bigint::operator[] (int i) const {
    if ((i < 0) || (i >= CAPACTIY))
        return 0;
    else
        return digit[i];
}


 
//////////////////////////////////////////////////////////////////////
/// Addition
/// PRE:  MAX(numberOfDigits(), rhs.numbersOfDigits()) + 1 < CAPACITY
/// POST: RETVAL == object + rhs 
/// 
bigint bigint::operator+(const bigint& rhs) const {
    int    carry = 0;
    bigint sum;

    for (int i=0; i<CAPACTIY; ++i) {
        sum.digit[i] = (carry + digit[i] + rhs.digit[i]) % 10;
        carry = (carry + digit[i] + rhs.digit[i]) / 10;
    }
    return sum;
}

bigint operator+  (int lhs,          const bigint& rhs) {return bigint(lhs) + rhs;};
bigint operator+  (const char lhs[], const bigint& rhs) {return bigint(lhs) + rhs;};



//////////////////////////////////////////////////////////////////////
/// PRE:  numberOfDigits() + power < CAPACITY
/// POST: RETVAL == object * 10^power
/// 
bigint bigint::times10(int power) const {
    bigint product;
    
    for (int i=0; i<CAPACTIY-power; ++i)
        product.digit[i+power] = digit[i];
    
    return product;
}

//////////////////////////////////////////////////////////////////////
/// Checks for lhs * 0..9
/// PRE:  numberOfDigits() * rhs.numbersOfDigits() < CAPACITY
/// POST: RETVAL == object * digit
/// 
///
bigint bigint::timesDigit(int rhs) const {
    bigint product;

    if (rhs > 9)  return *this * bigint(rhs);
    if (rhs == 0) return product;

    int carry = 0;
    for (int i=0; i<CAPACTIY; ++i) {
        product.digit[i] = ((digit[i] * rhs) + carry) % 10;
        carry = ((digit[i] * rhs) + carry) / 10;
    }
    return product;
}

//////////////////////////////////////////////////////////////////////
/// Multiplacation
/// PRE:  numberOfDigits() * rhs.numbersOfDigits() < CAPACITY
/// POST: RETVAL == object * x
///
bigint bigint::operator*(const bigint& x) const {
    bigint product;
    
    for (int i=0; i<CAPACTIY; ++i) {
        bigint temp;
        temp = timesDigit(x[i]);
        product = product + temp.times10(i);
    }
    return product;
}

bigint operator*  (int lhs,          const bigint& rhs) {return rhs * lhs;};
bigint operator*  (const char lhs[], const bigint& rhs) {return bigint(lhs) * rhs;};


//////////////////////////////////////////////////////////////////////
///
bool bigint::operator==(const bigint& x) const {
    for (int i=0; i<CAPACTIY; ++i)
        if (digit[i] != x.digit[i]) return false;
    return true;
}

 
//////////////////////////////////////////////////////////////////////
/// PRE:  in.open() && contains digit(s) followed by ;
/// POST: bigint is read into x from in until ;
/// 
std::istream& operator>>(std::istream& in, bigint& x) { 
    char temp[CAPACTIY];
    char ch = ';';
    
    int i = 0;
    if (!in.eof()) in >> ch;
    while ((ch != ';') && (!in.eof())) {
        temp[i++] = ch;
        in >> ch;
    }
    temp[i] = 0;
    x = bigint(temp);

    return in;
}




 
//////////////////////////////////////////////////////////////////////
/// PRE:  <none> 
/// POST: x is written to out
/// 
std::ostream& operator<<(std::ostream& out, const bigint& x) {
    bool leadingZero = true;
    for (int i = CAPACTIY-1; i>=0; --i) {
        if (x[i] != 0) leadingZero = false;
        if (!leadingZero) {
            out.ios_base::width(1);
            out << x[i];
        }
    }
    if (leadingZero) out << "0";

    return out;
}


//////////////////////////////////////////////////////////////////////
// Prints out the index and value for the entire array.
//
void bigint::debugPrint(std::ostream& out) {
    for (int i = CAPACTIY-1; i>=0; --i) {
        out << "|";
        out.ios_base::width(2);
        out << i;
    }
    out << "|" << std::endl;
    for (int i = CAPACTIY-1; i>=0; --i) {
        out << "|";
        out.ios_base::width(2);
        out << digit[i];
    }
    out << "|" << std::endl;
}













