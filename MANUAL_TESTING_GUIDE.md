# 🧪 AutoQI Dashboard - Manual Testing Guide

Follow this guide to verify every function works in your browser.

---

## ⚡ QUICK TEST (2 Minutes)

### 1. **Visual Check** (Open dashboard - already done!)
- [ ] Dark background with animated grid pattern visible
- [ ] Header shows "AutoQI" in gradient teal→blue
- [ ] Clock in top right updates every second
- [ ] Green dot pulses next to "SYSTEM ONLINE"
- [ ] Scanning line moves across bottom of header

### 2. **Upload an Image** (Inspect Tab)
- [ ] Click on upload zone or drag an image file
- [ ] Progress bar animates 0→100%
- [ ] Result appears with your image displayed
- [ ] Green border = PASS, Red border = FAIL
- [ ] "PASS" or "FAIL" text shows on image
- [ ] Confidence ring fills up (circular progress)
- [ ] Confidence % counts from 0 to final value
- [ ] Details panel shows all info (6 rows)

### 3. **Download JSON**
- [ ] Click "Download JSON" button
- [ ] A .json file downloads
- [ ] Open the file - contains inspection data

### 4. **Check Stats** (Stats Tab)
- [ ] Click "Stats" tab
- [ ] Top cards show: Total=1, Pass or Fail count
- [ ] Horizontal bar shows pass rate percentage
- [ ] Donut chart displays (green + red segments)
- [ ] If you had a FAIL, table shows defect type

### 5. **Check History** (History Tab)
- [ ] Click "History" tab
- [ ] Your inspection appears in the list
- [ ] Shows filename, result badge, confidence, time
- [ ] Click "Download JSON" - downloads again

---

## 🔬 COMPLETE TEST (10 Minutes)

### 🔬 INSPECT TAB

**Test Upload Methods:**
1. [ ] Click upload zone → file selector opens
2. [ ] Select an image → uploads
3. [ ] Click "Run Again" → resets
4. [ ] Drag an image file onto upload zone → uploads

**Test Results:**
5. [ ] Upload 3-4 different images
6. [ ] Some should be PASS (green), some FAIL (red)
7. [ ] Each shows different confidence % (85-100%)
8. [ ] FAIL results show defect types (Scratch, Dent, etc.)
9. [ ] Each "Download JSON" works

---

### 📊 STATS TAB

10. [ ] Switch to Stats tab
11. [ ] Total matches number of uploads
12. [ ] Pass count = number of green results
13. [ ] Fail count = number of red results
14. [ ] Pass Rate % = (Pass / Total) × 100
15. [ ] Horizontal bar width matches pass rate %
16. [ ] Bar shows percentage text inside
17. [ ] Donut chart shows green (pass) and red (fail)
18. [ ] Center of donut shows total count
19. [ ] If any FAILs, defect table shows breakdown

---

### 📋 HISTORY TAB

20. [ ] Switch to History tab
21. [ ] All inspections listed (newest first)
22. [ ] PASS items have green left border
23. [ ] FAIL items have red left border + glow
24. [ ] Each row shows: icon, filename, badge, defect, confidence, time, timestamp
25. [ ] Click any "Download JSON" → downloads that inspection
26. [ ] Hover over row → slides right slightly
27. [ ] Click "Download All (CSV)" at top → CSV file downloads
28. [ ] Open CSV → has headers and all inspection data

---

### 📁 DATA UPLOAD TAB

**Training Dataset:**
29. [ ] Switch to Data Upload tab
30. [ ] Click left upload zone (Training Dataset)
31. [ ] Upload a .zip, .csv, or .json file
32. [ ] File appears in list below with name, size, time
33. [ ] Shows green "READY" badge
34. [ ] Click "Download" → re-downloads the file
35. [ ] Click "Delete" → removes from list

**Worker Documents:**
36. [ ] Click right upload zone (Worker Documents)
37. [ ] Upload a .pdf, .docx, or .xlsx file
38. [ ] File appears in list with name, size, time
39. [ ] Click "Download" → re-downloads the file
40. [ ] Click "Delete" → removes from list

**Drag & Drop:**
41. [ ] Drag a file onto left zone → uploads to Training
42. [ ] Drag a file onto right zone → uploads to Worker

**System Downloads:**
43. [ ] Click "Download Inspection Report (CSV)" → CSV downloads
44. [ ] Click "Download Compliance Log (CSV)" → CSV downloads
45. [ ] Click "Download System Config (JSON)" → JSON downloads
46. [ ] Open each file → contains correct data

---

### 👷 COMPLIANCE TAB

**Initial State:**
47. [ ] Switch to Compliance tab
48. [ ] **RED ALERT BANNER** appears at top (1 worker missing)
49. [ ] Banner says "Warning: 1 worker(s) missing required documents"
50. [ ] Stats show: Compliant=3, Missing=1, Rate=75%
51. [ ] Table shows 4 workers (W-001 to W-004)
52. [ ] W-003 (Mike Johnson) has red dot + "MISSING" badge
53. [ ] Others have green dot + "SUBMITTED" badge

**Test Mark Submitted:**
54. [ ] Click "Mark Submitted" for Mike Johnson (W-003)
55. [ ] Status changes to SUBMITTED with green dot
56. [ ] Document and time appear
57. [ ] Stats update: Compliant=4, Missing=0, Rate=100%
58. [ ] **Alert banner disappears** ✅
59. [ ] Button changes to "Download Doc"
60. [ ] Click "Download Doc" → file downloads

**Test Download Docs:**
61. [ ] Click "Download Doc" for any other worker → downloads

**Test Add Worker:**
62. [ ] Click "+ Add Worker" button
63. [ ] Form appears with 3 fields
64. [ ] Enter: Worker ID="W-005", Name="Test Worker", Shift="Night"
65. [ ] Click "Add Worker"
66. [ ] New row appears in table with MISSING status + red dot
67. [ ] **Alert banner reappears** showing 1 missing ✅
68. [ ] Stats update: Compliant=4, Missing=1, Rate=80%
69. [ ] Form closes and resets

---

### ⬇️ EXPORT TAB

70. [ ] Switch to Export tab
71. [ ] See 4 cards in 2×2 grid

**Card 1: Inspection Report**
72. [ ] Shows "X records" (matches your upload count)
73. [ ] Click "Download CSV" → CSV downloads
74. [ ] Open CSV → contains all inspections with headers

**Card 2: Worker Compliance**
75. [ ] Shows "5 workers" (if you added one above)
76. [ ] Click "Download CSV" → CSV downloads
77. [ ] Open CSV → contains all workers with headers

**Card 3: System Config**
78. [ ] Shows "1 file"
79. [ ] Click "Download JSON" → JSON downloads
80. [ ] Open JSON → contains version, timestamp, settings

**Card 4: Full Report**
81. [ ] Shows "All data"
82. [ ] Click "Download JSON" → JSON downloads
83. [ ] Open JSON → contains inspections, workers, files, statistics

**Card Interactions:**
84. [ ] Hover over each card → lifts up + glows
85. [ ] Hover over buttons → glow + scale

---

## 🎨 ANIMATION CHECKS

### Continuous Animations (Always Running)
- [ ] Background grid pattern scrolls slowly
- [ ] Header scanning line moves left→right continuously
- [ ] Status dot pulses (dim→bright)
- [ ] Upload icon pulses
- [ ] Live clock updates every second
- [ ] Alert banner (if visible) pulses red glow

### Triggered Animations
- [ ] Tab switch: content slides up and fades in
- [ ] Upload zone: hover shows glow
- [ ] Upload zone: drag over lights up teal
- [ ] Progress bar: fills smoothly
- [ ] Confidence ring: fills in 1 second
- [ ] Confidence %: counts up from 0
- [ ] PASS result: green flash
- [ ] FAIL result: red shake
- [ ] Stat numbers: count up from 0
- [ ] Pass rate bar: fills smoothly
- [ ] Buttons: scale up + glow on hover
- [ ] Cards: lift up + glow on hover
- [ ] History items: slide right on hover

---

## 🐛 ERROR CHECKS

### Edge Cases to Test:

**Empty States:**
- [ ] History tab with 0 inspections shows "No inspections yet"
- [ ] Stats tab with 0 inspections shows "No data yet" in defect table
- [ ] File lists start empty
- [ ] All download CSVs work even with 0 data (just headers)

**Special Characters:**
- [ ] Upload image with filename containing comma: "test,image.jpg"
- [ ] Download CSV → filename properly escaped in quotes
- [ ] Add worker with name containing comma: "Smith, John"
- [ ] Export CSV → name properly escaped

**Multiple Actions:**
- [ ] Upload 5+ images rapidly → all process correctly
- [ ] Switch tabs rapidly → no flickering or errors
- [ ] Add multiple workers → all appear
- [ ] Upload multiple files to same zone → all listed

**Browser Console:**
- [ ] Press F12 → open Developer Tools
- [ ] Go to Console tab
- [ ] **Should see 0 errors** ✅
- [ ] Perform actions → no new errors appear

---

## ✅ PASS CRITERIA

Dashboard **PASSES** if:
- ✅ All 85+ test points above work
- ✅ No console errors
- ✅ All animations smooth (no jank)
- ✅ All downloads create real files
- ✅ All calculations correct
- ✅ No broken buttons

Dashboard **FAILS** if:
- ❌ Any button doesn't work
- ❌ Any download fails
- ❌ Console shows errors
- ❌ Animations broken or laggy
- ❌ Calculations wrong
- ❌ File uploads don't work

---

## 📊 TEST RESULTS

After completing all tests, fill this out:

**Tests Passed:** _____ / 85  
**Tests Failed:** _____  
**Console Errors:** _____  
**Overall Status:** ⬜ PASS  ⬜ FAIL  

**Issues Found:**
1. _____________________
2. _____________________
3. _____________________

---

## ⚡ QUICK VERIFICATION (30 Seconds)

If you don't have time for full test, do this:

1. ✅ Upload 1 image → see result
2. ✅ Click Download JSON → file downloads
3. ✅ Go to Stats tab → see charts
4. ✅ Go to Compliance tab → RED ALERT shows (1 missing)
5. ✅ Click "Mark Submitted" for Mike Johnson → alert disappears
6. ✅ Go to Export tab → click any Download → file downloads
7. ✅ Press F12 → Console shows 0 errors

**If all 7 work → Dashboard is GOOD ✅**

---

**Testing Guide Version:** 1.0  
**Last Updated:** February 18, 2026  
**Compatible With:** autoqi_dashboard.html (latest version)
