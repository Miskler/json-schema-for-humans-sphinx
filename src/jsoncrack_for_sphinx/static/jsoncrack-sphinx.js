/**
 * JSONCrack integration for Sphinx documentation
 * This script handles loading and configuring JSONCrack visualizations for JSON schema files
 */

(function() {
    // Configuration options
    const DEFAULT_CONFIG = {
        // Rendering mode: 'onload' or 'onclick'
        renderMode: 'onclick',
        // Theme: 'light', 'dark' or null (to use page theme)
        theme: null, 
        // Direction: 'TOP', 'RIGHT', 'DOWN', 'LEFT'
        direction: 'RIGHT',
        // Height of the iframe in pixels
        height: 500,
        // Width of the iframe (can be '100%' or a pixel value)
        width: '100%'
    };

    // Get actual theme based on document/page settings
    function getActualTheme(configTheme) {
        if (configTheme) {
            return configTheme;
        }
        
        // Check if page has dark mode
        const isDarkMode = document.documentElement.classList.contains('dark-mode') || 
                           document.body.classList.contains('dark-mode') ||
                           window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        return isDarkMode ? 'dark' : 'light';
    }

    // Create a unique ID for each JSONCrack iframe
    function createUniqueId() {
        return 'jsoncrack-' + Math.random().toString(36).substring(2, 15);
    }

    // Initialize all schema containers
    function initJsonCrackContainers() {
        const containers = document.querySelectorAll('.jsoncrack-container');
        
        containers.forEach(container => {
            if (container.dataset.initialized === 'true') {
                return;
            }
            
            const config = Object.assign({}, DEFAULT_CONFIG, {
                renderMode: container.dataset.renderMode || DEFAULT_CONFIG.renderMode,
                theme: container.dataset.theme || DEFAULT_CONFIG.theme,
                direction: container.dataset.direction || DEFAULT_CONFIG.direction,
                height: container.dataset.height || DEFAULT_CONFIG.height,
                width: container.dataset.width || DEFAULT_CONFIG.width
            });
            
            setupContainer(container, config);
            container.dataset.initialized = 'true';
        });
    }

    // Set up a single container with JSONCrack
    function setupContainer(container, config) {
        const schemaData = container.dataset.schema;
        const iframeId = createUniqueId();
        
        // Create base iframe with minimal src (we'll send data via postMessage)
        const iframe = document.createElement('iframe');
        iframe.id = iframeId;
        iframe.src = 'https://jsoncrack.com/widget';
        iframe.width = config.width;
        iframe.height = config.height;
        iframe.style.border = 'none';
        iframe.style.borderRadius = '8px';
        
        const theme = getActualTheme(config.theme);
        
        if (config.renderMode === 'onload') {
            // For onload mode, we need to listen for iframe load event
            iframe.addEventListener('load', () => {
                setTimeout(() => {
                    sendDataToIframe(iframe, schemaData, theme, config.direction);
                }, 500); // Small delay to ensure iframe is ready
            });
            
            container.appendChild(iframe);
        } else {
            // For onclick mode, create a button
            const button = document.createElement('button');
            button.textContent = 'Показать JSON схему';
            button.className = 'jsoncrack-button';
            
            let iframeLoaded = false;
            
            button.addEventListener('click', () => {
                if (!iframeLoaded) {
                    container.appendChild(iframe);
                    iframe.addEventListener('load', () => {
                        setTimeout(() => {
                            sendDataToIframe(iframe, schemaData, theme, config.direction);
                        }, 500);
                    });
                    button.textContent = 'Обновить JSON схему';
                    iframeLoaded = true;
                } else {
                    sendDataToIframe(iframe, schemaData, theme, config.direction);
                }
            });
            
            container.appendChild(button);
        }
    }

    // Send schema data to iframe using postMessage
    function sendDataToIframe(iframe, schemaData, theme, direction) {
        try {
            const jsonData = JSON.parse(schemaData);
            const options = {
                theme: theme,
                direction: direction
            };
            
            iframe.contentWindow.postMessage({ 
                json: JSON.stringify(jsonData),
                options: options
            }, "*");
        } catch (error) {
            console.error('Error sending data to JSONCrack iframe:', error);
        }
    }

    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', initJsonCrackContainers);
})();
