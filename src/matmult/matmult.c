/* BEEBS matmult benchmark

   Copyright (C) 2014 Embecosm Limited and University of Bristol

   Contributor James Pallister <james.pallister@bristol.ac.uk>

   This file is part of the Bristol/Embecosm Embedded Benchmark Suite.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program. If not, see <http://www.gnu.org/licenses/>. */

/* Original code from: WCET Benchmarks,
       http://www.mrtc.mdh.se/projects/wcet/benchmarks.html
   Permission to license under GPL obtained by email from Björn Lisper
 */

/* $Id: matmult.c,v 1.2 2005/04/04 11:34:58 csg Exp $ */

/* matmult.c */
/* was mm.c! */


/*----------------------------------------------------------------------*
 * To make this program compile under our assumed embedded environment,
 * we had to make several changes:
 * - Declare all functions in ANSI style, not K&R.
 *   this includes adding return types in all cases!
 * - Declare function prototypes
 * - Disable all output
 * - Disable all UNIX-style includes
 *
 * This is a program that was developed from mm.c to matmult.c by
 * Thomas Lundqvist at Chalmers.
 *----------------------------------------------------------------------*/
#ifdef MATMULT_FLOAT
#include <math.h>
#endif /* MATMULT_FLOAT */

#include "support.h"

/* This scale factor will be changed to equalise the runtime of the
   benchmarks. */
#ifdef MATMULT_FLOAT
#define SCALE_FACTOR    (REPEAT_FACTOR >> 5)
#define UPPERLIMIT 10
typedef float matrix [UPPERLIMIT][UPPERLIMIT];
#define RANDOM_VALUE ((float) RandomInteger () / 10.0)
#define ZERO 0.0
#define MOD_SIZE 255

int
values_match (float v1, float v2)
{
  if (v1 != v2)
    {
      int exp;
      float diff;

      /* Ignore the least significant bit of the mantissa
       * to account for any loss of precision due to floating point
       * operations */
      frexpf(v1, &exp);
      diff = fabsf(v1 - v2);
      /* TODO: Fix for big endian */
      if (diff > (1 << exp)) {
	return 0;
      }
    }

  return 1;
}

#elif defined MATMULT_INT
#define SCALE_FACTOR    (REPEAT_FACTOR >> 6)
#define UPPERLIMIT 20
#define RANDOM_VALUE (RandomInteger ())
#define ZERO 0
#define MOD_SIZE 8095
typedef long matrix [UPPERLIMIT][UPPERLIMIT];

int
values_match (long v1, long v2)
{
  return (v1 == v2);
}

#else
#error "No SCALE_FACTOR defined"
#endif

/*
 * MATRIX MULTIPLICATION BENCHMARK PROGRAM:
 * This program multiplies 2 square matrices resulting in a 3rd
 * matrix. It tests a compiler's speed in handling multidimensional
 * arrays and simple arithmetic.
 */




int Seed;
matrix ArrayA, ArrayB, ResultArray;

void Multiply(matrix A, matrix B, matrix Res);
void InitSeed(void);
void Test(matrix A, matrix B, matrix Res);
void Initialize(matrix Array);
int RandomInteger(void);

int main()
{
#ifdef MATMULT_FLOAT
   const matrix check_ResultArray = {
      {931.049988, 562.409973, 676.890015, 648.630005, 837.449951, 728.460022, 936.089905, 582.47998,  668.700012, 477.360016},
      {1296,       792.98999,  1174.41003, 411.120026, 1174.04993, 952.289978, 1285.56006, 1148.66992, 828,        751.139954},
      {903.150024, 596.609985, 937.890015, 665.279968, 1135.79993, 778.410034, 805.589966, 587.880005, 1077.29993, 540.809998},
      {552.599976, 630.539978, 1013.30994, 353.069977, 707.399963, 762.839966, 1052.45996, 924.119995, 822.599976, 631.439941},
      {1144.79993, 612.809998, 1148.48999, 759.329956, 913.949951, 808.110046, 1052.18994, 765.179993, 949.950073, 860.76001},
      {1147.04993, 698.940002, 885.059998, 386.370026, 1304.09998, 862.73999,  791.460083, 934.919983, 989.550049, 758.339966},
      {904.950012, 731.609924, 1078.73999, 819.179993, 1036.34998, 796.409973, 1067.94006, 453.780029, 809.099976, 644.309937},
      {850.049927, 784.890015, 1069.10999, 689.219971, 959.850037, 937.439941, 1162.26013, 1060.0199,  1216.79993, 916.290039},
      {931.049988, 562.409973, 676.890015, 648.630005, 837.449951, 728.460022, 936.089905, 582.47998,  668.700012, 477.360016},
      {1296,       792.98999,  1174.41003, 411.120026, 1174.04993, 952.289978, 1285.56006, 1148.66992, 828,        751.139954}
   };
#elif defined MATMULT_INT
   matrix check_ResultArray = {
      {299008155, 278859640, 356434140, 316921550, 310148425, 369422180, 363493165, 314898120, 265393255, 342605520, 351189510, 339881235, 349775180, 332407175, 271374935, 360571355, 379819765, 339962860, 292803300, 319827495},
      {329877145, 291981125, 401048060, 278783525, 282082465, 370360365, 368884060, 314521795, 281532195, 355215605, 326492030, 331864510, 351780495, 328795085, 293801430, 325047505, 368475005, 369699495, 317423945, 335623145},
      {303202970, 272968225, 321556960, 240573075, 253154915, 331007040, 303429310, 274738945, 251314570, 325003180, 267788730, 255740085, 323479270, 278638610, 260527380, 266528955, 357923505, 318823520, 292639045, 296822745},
      {400460115, 338721955, 429827245, 377196375, 343977185, 424491645, 408100270, 383138770, 287951090, 425885135, 412430240, 425799035, 333669015, 423454265, 326898965, 385980805, 423893150, 421973400, 354644930, 377191995},
      {373931090, 292903455, 419270170, 356978000, 351693485, 412365295, 394778645, 347003470, 296935015, 412317435, 378415940, 357822235, 368820015, 390193815, 316159290, 356614280, 421343825, 400229050, 309042630, 370578345},
      {327891910, 288890285, 386179205, 314131600, 271280030, 381268450, 366002830, 311422020, 238032935, 359765865, 343497000, 365298910, 339670885, 330258345, 267181750, 318222080, 363977145, 371448130, 280674840, 300097795},
      {391479675, 374246295, 405237000, 378863725, 358107020, 457906360, 473073775, 357307470, 280751150, 416429025, 404401795, 341162635, 381137700, 357736030, 361322270, 379200455, 393299535, 454201490, 378203410, 412279520},
      {382136315, 311258480, 426131495, 284829825, 292879485, 423241920, 360077595, 357380120, 274744490, 375918035, 358972940, 327101860, 367556640, 363677415, 309843565, 359728980, 428189450, 377638875, 306753880, 364851495},
      {415418065, 284159955, 456413745, 301027650, 342787935, 435160770, 401420645, 357046195, 291787915, 440625110, 434112565, 360638860, 403831690, 356003690, 348402340, 370360980, 448260375, 380795675, 320456055, 365799220},
      {335138715, 257603280, 352047195, 276898125, 256010360, 338378720, 314899220, 328290620, 253130940, 326652560, 307171915, 317363910, 291981290, 346373365, 233092590, 285109130, 329925400, 331533150, 279151730, 331678320},
      {328117795, 292920475, 369602210, 295823200, 274934965, 357240815, 366327235, 307467895, 240953095, 366926030, 340763755, 329354410, 336531920, 306489235, 308932630, 320077205, 334844080, 374713620, 335706695, 334940245},
      {325402585, 309877585, 369026780, 261873775, 251863330, 339276700, 379213305, 298297520, 246231685, 336545965, 354679875, 279576385, 337281960, 300810245, 290355975, 320829130, 353255570, 291247905, 314922340, 350649470},
      {367188625, 243323645, 357199125, 251075125, 291022520, 404397085, 296880900, 333473295, 246534675, 371566825, 334338695, 326282010, 299855975, 305611680, 299585995, 290686580, 388098135, 354047490, 268811010, 300774795},
      {386165170, 286955100, 398139660, 324383250, 330866765, 449518990, 403940885, 357447420, 258471895, 387874655, 387508430, 321833385, 332696120, 339630260, 322041380, 368333030, 367620255, 431054145, 323319020, 407249670},
      {443125645, 339868000, 499126885, 437279125, 372995090, 515742765, 500364785, 392145995, 288915670, 497925330, 490136055, 408352510, 435073645, 412961685, 390925630, 418545205, 465874380, 488341045, 345698620, 448423645},
      {321180270, 271615425, 277814585, 292908100, 275146590, 314603690, 315793735, 286549045, 217043870, 307386280, 308376380, 280296760, 272086745, 308176810, 239215330, 263679430, 286164055, 322446070, 284753295, 284483445},
      {389411030, 338198565, 429110090, 385274125, 363301850, 432488430, 399009490, 351771370, 302178555, 403999545, 459605510, 409328810, 392653905, 389707825, 342402385, 418969655, 441532090, 443883185, 362060900, 380626370},
      {245234330, 226732690, 286603290, 199830325, 262042800, 322337855, 281275340, 288052395, 205542505, 276205145, 246826410, 284868610, 260384080, 202462275, 232501410, 279952955, 313619265, 270682885, 237038325, 281062270},
      {353784680, 321355165, 403458490, 322727125, 341452075, 384460505, 414371440, 348951870, 285603105, 398078620, 385303910, 356217410, 350776430, 362338275, 338092935, 388634955, 393937840, 362511785, 379448275, 386488920},
      {469268630, 381624415, 460637690, 350851775, 326930600, 464558605, 458079940, 368923345, 325959180, 470384345, 455095285, 399817360, 420989805, 360067225, 366408910, 369932005, 467833590, 473619585, 426808550, 407822620}
   };
#else
   #error "No matrix initialisation data."
#endif

   int n;
   InitSeed();

   initialise_board();
   start_trigger();

   for(n = 0; n < SCALE_FACTOR; ++n)
      Test(ArrayA, ArrayB, ResultArray);

   stop_trigger();

   int to_return = 0;
   for (int i = 0; i < UPPERLIMIT; i++) {
      for (int j = 0; j < UPPERLIMIT; j++) {
	if (!values_match (ResultArray[i][j], check_ResultArray[i][j]))
	  {
               to_return = -1;
               break;
	  }
      }
   }

   return to_return;
}


/*
 * Initializes the seed used in the random number generator.
 */
void InitSeed(void)
{
   Seed = 0;
}

/*
 * Runs a multiplication test on an array.  Calculates and prints the
 * time it takes to multiply the matrices.
 */
void Test(matrix A, matrix B, matrix Res)
{
   int OuterIndex, InnerIndex;

   for (OuterIndex = 0; OuterIndex < UPPERLIMIT; OuterIndex++)
      for (InnerIndex = 0; InnerIndex < UPPERLIMIT; InnerIndex++)
         A[OuterIndex][InnerIndex] = RANDOM_VALUE;
   for (OuterIndex = 0; OuterIndex < UPPERLIMIT; OuterIndex++)
      for (InnerIndex = 0; InnerIndex < UPPERLIMIT; InnerIndex++)
         B[OuterIndex][InnerIndex] = RANDOM_VALUE;

   Multiply(A, B, Res);
}

/*
 * Generates random integers between 0 and 8095
 */
int RandomInteger(void)
{
   Seed = ((Seed * 133) + 81) % MOD_SIZE;
   return (Seed);
}

/*
 * Multiplies arrays A and B and stores the result in ResultArray.
 */
void Multiply(matrix A, matrix B, matrix Res)
{
   register int Outer, Inner, Index;

   for (Outer = 0; Outer < UPPERLIMIT; Outer++)
      for (Inner = 0; Inner < UPPERLIMIT; Inner++)
      {
         Res [Outer][Inner] = ZERO;
         for (Index = 0; Index < UPPERLIMIT; Index++)
            Res[Outer][Inner] += A[Outer][Index] * B[Index][Inner];
      }
}

/* vim: set ts=3 sw=3 et: */
