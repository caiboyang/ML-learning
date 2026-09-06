// Paper v3 Tables 1 and 6. Transcribed from arXiv HTML; means and sample SD.
const SCALE_DATA = {
  "warehouse": {
    "source": "S4.T1",
    "rows": [
      {
        "t": 10,
        "series": 0,
        "score": 0.9,
        "scoreSD": 0.02,
        "prompt": 3249,
        "promptSD": 94,
        "tokens": 9438,
        "tokensSD": 371
      },
      {
        "t": 10,
        "series": 1,
        "score": 1.0,
        "scoreSD": 0.0,
        "prompt": 3300,
        "promptSD": 123,
        "tokens": 9972,
        "tokensSD": 204
      },
      {
        "t": 10,
        "series": 2,
        "score": 1.0,
        "scoreSD": 0.0,
        "prompt": 3430,
        "promptSD": 42,
        "tokens": 10337,
        "tokensSD": 299
      },
      {
        "t": 10,
        "series": 3,
        "score": 1.0,
        "scoreSD": 0.0,
        "prompt": 1775,
        "promptSD": 74,
        "tokens": 5870,
        "tokensSD": 131
      },
      {
        "t": 25,
        "series": 0,
        "score": 0.92,
        "scoreSD": 0.02,
        "prompt": 6052,
        "promptSD": 192,
        "tokens": 42689,
        "tokensSD": 2238
      },
      {
        "t": 25,
        "series": 1,
        "score": 0.99,
        "scoreSD": 0.0,
        "prompt": 6357,
        "promptSD": 203,
        "tokens": 43067,
        "tokensSD": 1948
      },
      {
        "t": 25,
        "series": 2,
        "score": 1.0,
        "scoreSD": 0.0,
        "prompt": 5858,
        "promptSD": 301,
        "tokens": 41238,
        "tokensSD": 3196
      },
      {
        "t": 25,
        "series": 3,
        "score": 1.0,
        "scoreSD": 0.0,
        "prompt": 1736,
        "promptSD": 49,
        "tokens": 14714,
        "tokensSD": 564
      },
      {
        "t": 50,
        "series": 0,
        "score": 0.88,
        "scoreSD": 0.04,
        "prompt": 11931,
        "promptSD": 346,
        "tokens": 171658,
        "tokensSD": 6978
      },
      {
        "t": 50,
        "series": 1,
        "score": 0.93,
        "scoreSD": 0.03,
        "prompt": 7582,
        "promptSD": 283,
        "tokens": 131455,
        "tokensSD": 6841
      },
      {
        "t": 50,
        "series": 2,
        "score": 0.94,
        "scoreSD": 0.0,
        "prompt": 11594,
        "promptSD": 438,
        "tokens": 170992,
        "tokensSD": 7918
      },
      {
        "t": 50,
        "series": 3,
        "score": 0.96,
        "scoreSD": 0.01,
        "prompt": 1773,
        "promptSD": 53,
        "tokens": 30151,
        "tokensSD": 1231
      },
      {
        "t": 100,
        "series": 0,
        "score": 0.84,
        "scoreSD": 0.07,
        "prompt": 36362,
        "promptSD": 1304,
        "tokens": 1245413,
        "tokensSD": 53241
      },
      {
        "t": 100,
        "series": 1,
        "score": 0.87,
        "scoreSD": 0.05,
        "prompt": 29607,
        "promptSD": 978,
        "tokens": 1082154,
        "tokensSD": 83212
      },
      {
        "t": 100,
        "series": 2,
        "score": 0.91,
        "scoreSD": 0.02,
        "prompt": 31354,
        "promptSD": 831,
        "tokens": 1062387,
        "tokensSD": 53839
      },
      {
        "t": 100,
        "series": 3,
        "score": 0.94,
        "scoreSD": 0.01,
        "prompt": 1905,
        "promptSD": 93,
        "tokens": 65408,
        "tokensSD": 5431
      },
      {
        "t": 200,
        "series": 0,
        "score": 0.74,
        "scoreSD": 0.14,
        "prompt": 48007,
        "promptSD": 2092,
        "tokens": 2608755,
        "tokensSD": 102415
      },
      {
        "t": 200,
        "series": 1,
        "score": 0.84,
        "scoreSD": 0.09,
        "prompt": 84364,
        "promptSD": 3446,
        "tokens": 6175509,
        "tokensSD": 294089
      },
      {
        "t": 200,
        "series": 2,
        "score": 0.88,
        "scoreSD": 0.03,
        "prompt": 72305,
        "promptSD": 3096,
        "tokens": 5041164,
        "tokensSD": 346925
      },
      {
        "t": 200,
        "series": 3,
        "score": 0.94,
        "scoreSD": 0.02,
        "prompt": 1811,
        "promptSD": 184,
        "tokens": 122384,
        "tokensSD": 4522
      }
    ]
  },
  "software": {
    "source": "Ax4.T6",
    "rows": [
      {
        "t": 10,
        "series": 0,
        "score": 0.89,
        "scoreSD": 0.11,
        "prompt": 3411,
        "promptSD": 197,
        "tokens": 11670,
        "tokensSD": 841
      },
      {
        "t": 10,
        "series": 1,
        "score": 0.93,
        "scoreSD": 0.09,
        "prompt": 4379,
        "promptSD": 234,
        "tokens": 15732,
        "tokensSD": 562
      },
      {
        "t": 10,
        "series": 2,
        "score": 1.0,
        "scoreSD": 0.0,
        "prompt": 4200,
        "promptSD": 321,
        "tokens": 14120,
        "tokensSD": 318
      },
      {
        "t": 10,
        "series": 3,
        "score": 1.0,
        "scoreSD": 0.0,
        "prompt": 2298,
        "promptSD": 134,
        "tokens": 7608,
        "tokensSD": 149
      },
      {
        "t": 25,
        "series": 0,
        "score": 0.84,
        "scoreSD": 0.05,
        "prompt": 11754,
        "promptSD": 608,
        "tokens": 111970,
        "tokensSD": 3314
      },
      {
        "t": 25,
        "series": 1,
        "score": 0.89,
        "scoreSD": 0.07,
        "prompt": 9399,
        "promptSD": 317,
        "tokens": 94629,
        "tokensSD": 2839
      },
      {
        "t": 25,
        "series": 2,
        "score": 0.94,
        "scoreSD": 0.03,
        "prompt": 14016,
        "promptSD": 586,
        "tokens": 128702,
        "tokensSD": 3863
      },
      {
        "t": 25,
        "series": 3,
        "score": 0.88,
        "scoreSD": 0.08,
        "prompt": 2545,
        "promptSD": 556,
        "tokens": 21920,
        "tokensSD": 431
      },
      {
        "t": 50,
        "series": 0,
        "score": 0.71,
        "scoreSD": 0.14,
        "prompt": 23136,
        "promptSD": 911,
        "tokens": 462118,
        "tokensSD": 13764
      },
      {
        "t": 50,
        "series": 1,
        "score": 0.65,
        "scoreSD": 0.12,
        "prompt": 35550,
        "promptSD": 2412,
        "tokens": 688182,
        "tokensSD": 23539
      },
      {
        "t": 50,
        "series": 2,
        "score": 0.74,
        "scoreSD": 0.08,
        "prompt": 31166,
        "promptSD": 3231,
        "tokens": 577027,
        "tokensSD": 27293
      },
      {
        "t": 50,
        "series": 3,
        "score": 0.86,
        "scoreSD": 0.04,
        "prompt": 2545,
        "promptSD": 63,
        "tokens": 45100,
        "tokensSD": 894
      },
      {
        "t": 100,
        "series": 0,
        "score": 0.53,
        "scoreSD": 0.16,
        "prompt": 46270,
        "promptSD": 1847,
        "tokens": 1848500,
        "tokensSD": 55391
      },
      {
        "t": 100,
        "series": 1,
        "score": 0.57,
        "scoreSD": 0.05,
        "prompt": 71100,
        "promptSD": 5836,
        "tokens": 2752700,
        "tokensSD": 82467
      },
      {
        "t": 100,
        "series": 2,
        "score": 0.63,
        "scoreSD": 0.1,
        "prompt": 62330,
        "promptSD": 2488,
        "tokens": 2308000,
        "tokensSD": 35183
      },
      {
        "t": 100,
        "series": 3,
        "score": 0.78,
        "scoreSD": 0.08,
        "prompt": 2545,
        "promptSD": 471,
        "tokens": 90200,
        "tokensSD": 2792
      }
    ]
  }
};
