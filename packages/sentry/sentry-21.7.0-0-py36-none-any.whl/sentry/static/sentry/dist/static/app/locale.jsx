Object.defineProperty(exports, "__esModule", { value: true });
exports.tn = exports.tct = exports.t = exports.gettextComponentTemplate = exports.ngettext = exports.gettext = exports.format = exports.renderTemplate = exports.parseComponentTemplate = exports.setLocale = exports.toggleLocaleDebug = exports.setLocaleDebug = exports.DEFAULT_LOCALE_DATA = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var jed_1 = tslib_1.__importDefault(require("jed"));
var isArray_1 = tslib_1.__importDefault(require("lodash/isArray"));
var isObject_1 = tslib_1.__importDefault(require("lodash/isObject"));
var isString_1 = tslib_1.__importDefault(require("lodash/isString"));
var sprintf_js_1 = require("sprintf-js");
var localStorage_1 = tslib_1.__importDefault(require("app/utils/localStorage"));
var markerStyles = {
    background: '#ff801790',
    outline: '2px solid #ff801790',
};
var LOCALE_DEBUG = localStorage_1.default.getItem('localeDebug') === '1';
exports.DEFAULT_LOCALE_DATA = {
    '': {
        domain: 'sentry',
        lang: 'en',
        plural_forms: 'nplurals=2; plural=(n != 1);',
    },
};
function setLocaleDebug(value) {
    localStorage_1.default.setItem('localeDebug', value ? '1' : '0');
    // eslint-disable-next-line no-console
    console.log("Locale debug is: " + (value ? 'on' : 'off') + ". Reload page to apply changes!");
}
exports.setLocaleDebug = setLocaleDebug;
/**
 * Toggles the locale debug flag in local storage, but does _not_ reload the
 * page. The caller should do this.
 */
function toggleLocaleDebug() {
    var currentValue = localStorage_1.default.getItem('localeDebug');
    setLocaleDebug(currentValue !== '1');
}
exports.toggleLocaleDebug = toggleLocaleDebug;
/**
 * Global Jed locale object loaded with translations via setLocale
 */
var i18n = null;
/**
 * Set the current application locale.
 *
 * NOTE: This MUST be called early in the application before calls to any
 * translation functions, as this mutates a singleton translation object used
 * to lookup translations at runtime.
 */
function setLocale(translations) {
    i18n = new jed_1.default({
        domain: 'sentry',
        missing_key_callback: function () { },
        locale_data: {
            sentry: translations,
        },
    });
    return i18n;
}
exports.setLocale = setLocale;
/**
 * Helper to return the i18n client, and initialize for the default locale (English)
 * if it has otherwise not been initialized.
 */
function getClient() {
    if (!i18n) {
        // If this happens, it could mean that an import was added/changed where
        // locale initialization does not happen soon enough.
        var warning = new Error('Locale not set, defaulting to English');
        console.error(warning); // eslint-disable-line no-console
        Sentry.captureException(warning);
        return setLocale(exports.DEFAULT_LOCALE_DATA);
    }
    return i18n;
}
/**
 * printf style string formatting which render as react nodes.
 */
function formatForReact(formatString, args) {
    var nodes = [];
    var cursor = 0;
    // always re-parse, do not cache, because we change the match
    sprintf_js_1.sprintf.parse(formatString).forEach(function (match, idx) {
        if (isString_1.default(match)) {
            nodes.push(match);
            return;
        }
        var arg = null;
        if (match[2]) {
            arg = args[0][match[2][0]];
        }
        else if (match[1]) {
            arg = args[parseInt(match[1], 10) - 1];
        }
        else {
            arg = args[cursor++];
        }
        // this points to a react element!
        if (React.isValidElement(arg)) {
            nodes.push(React.cloneElement(arg, { key: idx }));
        }
        else {
            // not a react element, fuck around with it so that sprintf.format
            // can format it for us.  We make sure match[2] is null so that we
            // do not go down the object path, and we set match[1] to the first
            // index and then pass an array with two items in.
            match[2] = null;
            match[1] = 1;
            nodes.push(<span key={idx++}>{sprintf_js_1.sprintf.format([match], [null, arg])}</span>);
        }
    });
    return nodes;
}
/**
 * Determine if any arguments include React elements.
 */
function argsInvolveReact(args) {
    if (args.some(React.isValidElement)) {
        return true;
    }
    if (args.length !== 1 || !isObject_1.default(args[0])) {
        return false;
    }
    var componentMap = args[0];
    return Object.keys(componentMap).some(function (key) { return React.isValidElement(componentMap[key]); });
}
/**
 * Parses a template string into groups.
 *
 * The top level group will be keyed as `root`. All other group names will have
 * been extracted from the template string.
 */
function parseComponentTemplate(template) {
    var parsed = {};
    function process(startPos, group, inGroup) {
        var regex = /\[(.*?)(:|\])|\]/g;
        var buf = [];
        var satisfied = false;
        var match;
        var pos = (regex.lastIndex = startPos);
        // eslint-disable-next-line no-cond-assign
        while ((match = regex.exec(template)) !== null) {
            var substr = template.substr(pos, match.index - pos);
            if (substr !== '') {
                buf.push(substr);
            }
            var _a = tslib_1.__read(match, 3), fullMatch = _a[0], groupName = _a[1], closeBraceOrValueSeparator = _a[2];
            if (fullMatch === ']') {
                if (inGroup) {
                    satisfied = true;
                    break;
                }
                else {
                    pos = regex.lastIndex;
                    continue;
                }
            }
            if (closeBraceOrValueSeparator === ']') {
                pos = regex.lastIndex;
            }
            else {
                pos = regex.lastIndex = process(regex.lastIndex, groupName, true);
            }
            buf.push({ group: groupName });
        }
        var endPos = regex.lastIndex;
        if (!satisfied) {
            var rest = template.substr(pos);
            if (rest) {
                buf.push(rest);
            }
            endPos = template.length;
        }
        parsed[group] = buf;
        return endPos;
    }
    process(0, 'root', false);
    return parsed;
}
exports.parseComponentTemplate = parseComponentTemplate;
/**
 * Renders a parsed template into a React tree given a ComponentMap to use for
 * the parsed groups.
 */
function renderTemplate(template, components) {
    var idx = 0;
    function renderGroup(groupKey) {
        var e_1, _a;
        var _b;
        var children = [];
        var group = template[groupKey] || [];
        try {
            for (var group_1 = tslib_1.__values(group), group_1_1 = group_1.next(); !group_1_1.done; group_1_1 = group_1.next()) {
                var item = group_1_1.value;
                if (isString_1.default(item)) {
                    children.push(<span key={idx++}>{item}</span>);
                }
                else {
                    children.push(renderGroup(item.group));
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (group_1_1 && !group_1_1.done && (_a = group_1.return)) _a.call(group_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        // In case we cannot find our component, we call back to an empty
        // span so that stuff shows up at least.
        var reference = (_b = components[groupKey]) !== null && _b !== void 0 ? _b : <span key={idx++}/>;
        if (!React.isValidElement(reference)) {
            reference = <span key={idx++}>{reference}</span>;
        }
        var element = reference;
        return children.length === 0
            ? React.cloneElement(element, { key: idx++ })
            : React.cloneElement(element, { key: idx++ }, children);
    }
    return <React.Fragment>{renderGroup('root')}</React.Fragment>;
}
exports.renderTemplate = renderTemplate;
/**
 * mark is used to debug translations by visually marking translated strings.
 *
 * NOTE: This is a no-op and will return the node if LOCALE_DEBUG is not
 * currently enabled. See setLocaleDebug and toggleLocaleDebug.
 */
function mark(node) {
    if (!LOCALE_DEBUG) {
        return node;
    }
    // TODO(epurkhiser): Explain why we manually create a react node and assign
    // the toString function. This could likely also use better typing, but will
    // require some understanding of reacts internal types.
    var proxy = {
        $$typeof: Symbol.for('react.element'),
        type: 'span',
        key: null,
        ref: null,
        props: {
            style: markerStyles,
            children: isArray_1.default(node) ? node : [node],
        },
        _owner: null,
        _store: {},
    };
    proxy.toString = function () { return '✅' + node + '✅'; };
    return proxy;
}
/**
 * sprintf style string formatting. Does not handle translations.
 *
 * See the sprintf-js library [0] for specifics on the argument
 * parameterization format.
 *
 * [0]: https://github.com/alexei/sprintf.js
 */
function format(formatString, args) {
    if (argsInvolveReact(args)) {
        return formatForReact(formatString, args);
    }
    return sprintf_js_1.sprintf.apply(void 0, tslib_1.__spreadArray([formatString], tslib_1.__read(args)));
}
exports.format = format;
/**
 * Translates a string to the current locale.
 *
 * See the sprintf-js library [0] for specifics on the argument
 * parameterization format.
 *
 * [0]: https://github.com/alexei/sprintf.js
 */
function gettext(string) {
    var args = [];
    for (var _i = 1; _i < arguments.length; _i++) {
        args[_i - 1] = arguments[_i];
    }
    var val = getClient().gettext(string);
    if (args.length === 0) {
        return mark(val);
    }
    // XXX(ts): It IS possible to use gettext in such a way that it will return a
    // React.ReactNodeArray, however we currently rarely (if at all) use it in
    // this way, and usually just expect strings back.
    return mark(format(val, args));
}
exports.gettext = gettext;
exports.t = gettext;
/**
 * Translates a singular and plural string to the current locale. Supports
 * argument parameterization, and will use the first argument as the counter to
 * determine which message to use.
 *
 * See the sprintf-js library [0] for specifics on the argument
 * parameterization format.
 *
 * [0]: https://github.com/alexei/sprintf.js
 */
function ngettext(singular, plural) {
    var args = [];
    for (var _i = 2; _i < arguments.length; _i++) {
        args[_i - 2] = arguments[_i];
    }
    var countArg = 0;
    if (args.length > 0) {
        countArg = Math.abs(args[0]) || 0;
        // `toLocaleString` will render `999` as `"999"` but `9999` as `"9,999"`. This means that any call with `tn` or `ngettext` cannot use `%d` in the codebase but has to use `%s`.
        // This means a string is always being passed in as an argument, but `sprintf-js` implicitly coerces strings that can be parsed as integers into an integer.
        // This would break under any locale that used different formatting and other undesirable behaviors.
        if ((singular + plural).includes('%d')) {
            // eslint-disable-next-line no-console
            console.error(new Error('You should not use %d within tn(), use %s instead'));
        }
        else {
            args = tslib_1.__spreadArray([countArg.toLocaleString()], tslib_1.__read(args.slice(1)));
        }
    }
    // XXX(ts): See XXX in gettext.
    return mark(format(getClient().ngettext(singular, plural, countArg), args));
}
exports.ngettext = ngettext;
exports.tn = ngettext;
/**
 * special form of gettext where you can render nested react components in
 * template strings.
 *
 * ```jsx
 * gettextComponentTemplate('Welcome. Click [link:here]', {
 *   root: <p/>,
 *   link: <a href="#" />,
 * });
 * ```
 *
 * The root string is always called "root", the rest is prefixed with the name
 * in the brackets
 *
 * You may recursively nest additional groups within the grouped string values.
 */
function gettextComponentTemplate(template, components) {
    var tmpl = parseComponentTemplate(getClient().gettext(template));
    return mark(renderTemplate(tmpl, components));
}
exports.gettextComponentTemplate = gettextComponentTemplate;
exports.tct = gettextComponentTemplate;
//# sourceMappingURL=locale.jsx.map