package com.studentreadiness.app

import android.os.Bundle
import android.webkit.WebView
import android.webkit.WebViewClient
import android.webkit.WebChromeClient
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity
import android.app.DownloadManager
import android.net.Uri
import android.os.Environment
import android.webkit.URLUtil
import android.widget.Toast
import android.webkit.CookieManager

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        webView = WebView(this)
        setContentView(webView)

        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.settings.loadsImagesAutomatically = true

        webView.webViewClient = WebViewClient()
        webView.webChromeClient = WebChromeClient()
        webView.setDownloadListener { url, userAgent, contentDisposition, mimeType, contentLength ->

            val fileName = URLUtil.guessFileName(
                url,
                contentDisposition,
                mimeType
            )

            val request = DownloadManager.Request(Uri.parse(url))

            request.setTitle(fileName)
            request.setDescription("Downloading your assessment PDF")
            request.setMimeType(mimeType)

            request.addRequestHeader("User-Agent", userAgent)

            val cookies = CookieManager.getInstance().getCookie(url)
            if (cookies != null) {
                request.addRequestHeader("Cookie", cookies)
            }

            request.setNotificationVisibility(
                DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED
            )

            request.setDestinationInExternalPublicDir(
                Environment.DIRECTORY_DOWNLOADS,
                fileName
            )

            val downloadManager =
                getSystemService(DOWNLOAD_SERVICE) as DownloadManager

            downloadManager.enqueue(request)

            Toast.makeText(
                this,
                "Download started. Check Downloads folder.",
                Toast.LENGTH_LONG
            ).show()
        }

        webView.loadUrl("https://student-readiness-app-aj9fz8mcgjsvpqvlznqx6l.streamlit.app/Student_Assessment")

        onBackPressedDispatcher.addCallback(
            this,
            object : OnBackPressedCallback(true) {
                override fun handleOnBackPressed() {
                    if (webView.canGoBack()) {
                        webView.goBack()
                    } else {
                        finish()
                    }
                }
            }
        )
    }
}