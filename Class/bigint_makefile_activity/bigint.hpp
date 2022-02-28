 
//////////////////////////////////////////////////////////////////////
/// 
///             Software Development Laboratory <SDML> 
///                   Kent State University 
/// 
/// 
///   @file   : bigint.hpp
/// 
///   Project : 
/// 
///   Author  : J. Maletic
/// 
///   Date    : 8/16/2002
/// 
///   Purpose : Declaration of class 
/// 
/// 
//////////////////////////////////////////////////////////////////////
/// 
///  ================
/// 
///  Version History: 
/// 
///  - V 0.10  8/16/2002  Created
///            8/29/2017  updated
/// 
//////////////////////////////////////////////////////////////////////
 
#ifndef CS2_BIGINT_H_
#define CS2_BIGINT_H_

#include <fstream>
#include <iostream>

const int CAPACTIY = 200;

 
//////////////////////////////////////////////////////////////////////
///  CLASS INV: digit[i] == 0 || 1 || .. || 9
///
///  Positive numbers only.
///  bigint a = 345;
///  a.digit[CAPACITY-1 .. 3] == 0 && a.digit[2] == 3 && a.digit[1] == 4 && a.digit[0] == 5
///  
///  Description: A class to implement very large integer numbers 
///  
///
class bigint {
public:
            bigint        ();
            bigint        (int);
            bigint        (const char[]);
    bigint  operator+     (const bigint&) const;
    bigint  times10       (int)           const;
    bigint  timesDigit    (int)           const;
    bigint  operator*     (const bigint&) const;
    int     operator[]    (int)           const;
    int     numberOfDigits()              const;
    bool    operator==    (const bigint&) const;
    void    debugPrint    (std::ostream& out);

private:
    int     digit[CAPACTIY];
};

bigint        operator*     (int,           const bigint&);
bigint        operator*     (const char[],  const bigint&);
bigint        operator+     (int,           const bigint&);
bigint        operator+     (const char[],  const bigint&);
std::istream& operator>>    (std::istream&, bigint&);
std::ostream& operator<<    (std::ostream&, const bigint&);



#endif
