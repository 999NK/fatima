
// jQuery básico para resolver dependências
(function(global) {
    'use strict';
    
    function jQuery(selector) {
        return new jQuery.fn.init(selector);
    }
    
    jQuery.fn = jQuery.prototype = {
        init: function(selector) {
            this.length = 0;
            return this;
        },
        ready: function(fn) {
            if (document.readyState === 'complete' || document.readyState === 'interactive') {
                setTimeout(fn, 1);
            } else {
                document.addEventListener('DOMContentLoaded', fn);
            }
            return this;
        },
        each: function(fn) {
            return this;
        }
    };
    
    jQuery.fn.init.prototype = jQuery.fn;
    
    // Métodos estáticos básicos
    jQuery.extend = function() {
        var target = arguments[0] || {};
        for (var i = 1; i < arguments.length; i++) {
            var source = arguments[i];
            if (source) {
                for (var key in source) {
                    if (source.hasOwnProperty(key)) {
                        target[key] = source[key];
                    }
                }
            }
        }
        return target;
    };
    
    jQuery.noop = function() {};
    jQuery.isFunction = function(obj) {
        return typeof obj === 'function';
    };
    
    // Alias
    var $ = jQuery;
    
    // Expor globalmente
    global.jQuery = global.$ = jQuery;
    
})(window);

// WordPress compatibility
window.wp = window.wp || {};
window.wp.i18n = window.wp.i18n || {
    __: function(text) { return text; },
    _x: function(text) { return text; },
    _n: function(single, plural, number) { return number === 1 ? single : plural; }
};

// Adicionar suporte básico para outros scripts
window.wp.hooks = window.wp.hooks || {
    addAction: function() {},
    addFilter: function() {},
    doAction: function() {},
    applyFilters: function(tag, value) { return value; }
};
