# 📚 Setting Up Your Study Materials

The AI Study Tool works with **any subject or domain**. You just need to provide your own study materials!

## 🎯 How It Works

1. **Provide your PDFs and videos** via environment variables
2. **The tool ingests them** into a knowledge base
3. **Ask questions** about any topic in your materials
4. **Get answers** grounded in your specific content

## 📝 Configuration

### Step 1: Add PDF Documents

In your `.env` file, add PDF URLs:

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

After updating your content sources:

1. **Update `.env`** with new URLs
2. **Restart the backend**
3. **Or trigger re-ingestion** via API:
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

