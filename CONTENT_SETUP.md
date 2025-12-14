# 📚 Setting Up Your Study Materials

The AI Study Tool works with **any subject or domain**. You just need to provide your own study materials!

## 🎯 Easy Method (No Coding Required!)

### Using the Web Interface

1. **Start the app** (both frontend and backend)
2. **Open the "My Materials" tab** (first tab in the interface)
3. **Click "Add Content"** button
4. **Choose how to add content**:
   - **📄 Upload PDF**: Click to select a PDF file from your computer (up to 50MB)
   - **🔗 PDF URL**: Paste a Google Drive or direct PDF link
   - **▶️ YouTube Video**: Paste any YouTube video URL

5. **Add details** (optional):
   - Give it a title (e.g., "Chapter 5 - Physics")
   - Add a description

6. **Click "Add Source"** - The system processes it automatically!

### Features

- ✅ **Works on any device**: Desktop, tablet, mobile
- ✅ **Works in any browser**: Chrome, Firefox, Safari, Edge
- ✅ **No technical knowledge needed**: Just click and upload
- ✅ **Multiple sources**: Add as many PDFs and videos as you want
- ✅ **Easy management**: View, organize, and remove sources anytime

## 📝 Advanced Method (Environment Variables)

For advanced users, you can also configure via `.env` file:

### Step 1: Add PDF Documents

```env
# Single PDF
PDF_URL=https://drive.google.com/file/d/YOUR_FILE_ID/view

# Multiple PDFs (comma-separated)
PDF_URLS=https://drive.google.com/file/d/PDF1_ID/view,https://drive.google.com/file/d/PDF2_ID/view
```

**Supported PDF Sources:**
- Google Drive (shareable links)
- Direct PDF URLs
- Any publicly accessible PDF

### Step 2: Add YouTube Videos

```env
# Multiple videos (comma-separated)
YOUTUBE_VIDEOS=https://youtu.be/VIDEO_ID_1,https://www.youtube.com/watch?v=VIDEO_ID_2
```

**Note**: Videos must have transcripts available (most educational videos do).

### Step 3: Optional - Set Subject Name

```env
# Optional: Customize prompts for your subject
SUBJECT_NAME=Physics
# Or: Mathematics, History, Literature, Programming, etc.
```

## 🔄 Re-ingesting Content

When you add content through the UI, it automatically re-processes everything. 

For manual re-ingestion via API:
```bash
curl -X POST http://localhost:5000/api/ingest
```

## 📖 Example Configurations

### Example 1: Physics Course
```env
PDF_URLS=https://drive.google.com/file/d/physics-textbook/view
YOUTUBE_VIDEOS=https://youtu.be/physics-lecture-1,https://youtu.be/physics-lecture-2
SUBJECT_NAME=Physics
```

### Example 2: History Class
```env
PDF_URLS=https://drive.google.com/file/d/history-textbook/view,https://drive.google.com/file/d/primary-sources/view
YOUTUBE_VIDEOS=https://youtu.be/history-documentary
SUBJECT_NAME=World History
```

### Example 3: Programming Course
```env
PDF_URLS=https://drive.google.com/file/d/python-tutorial/view
YOUTUBE_VIDEOS=https://youtu.be/python-basics,https://youtu.be/python-advanced
SUBJECT_NAME=Python Programming
```

## ✅ Best Practices

1. **Use quality sources**: Well-structured PDFs and clear videos work best
2. **Multiple sources**: Combine textbooks, lecture notes, and videos
3. **Organize by topic**: Group related materials together
4. **Update regularly**: Re-ingest when you add new materials

## 🎓 Subject Examples

The tool works great for:
- **STEM**: Math, Physics, Chemistry, Biology, Computer Science
- **Humanities**: History, Literature, Philosophy, Languages
- **Social Sciences**: Economics, Psychology, Sociology, Political Science
- **Professional**: Business, Law, Medicine, Engineering
- **Creative**: Art History, Music Theory, Design

**Any subject works!** Just provide your materials.

## 🆘 Troubleshooting

### PDF Not Loading
- Ensure the PDF is publicly accessible
- For Google Drive: Make sure sharing is enabled
- Check the URL format is correct

### Video Transcript Not Available
- Some videos don't have transcripts
- Try a different video or add manual transcripts
- Educational channels usually have transcripts

### Content Not Appearing in Answers
- Wait for RAG initialization to complete
- Check backend logs for ingestion errors
- Verify URLs are correct in `.env`

