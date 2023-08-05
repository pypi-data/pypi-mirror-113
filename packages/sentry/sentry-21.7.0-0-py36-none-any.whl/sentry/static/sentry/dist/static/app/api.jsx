Object.defineProperty(exports, "__esModule", { value: true });
exports.Client = exports.hasProjectBeenRenamed = exports.initApiClientErrorHandling = exports.Request = void 0;
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var react_1 = require("@sentry/react");
var jquery_1 = tslib_1.__importDefault(require("jquery"));
var js_cookie_1 = tslib_1.__importDefault(require("js-cookie"));
var isUndefined_1 = tslib_1.__importDefault(require("lodash/isUndefined"));
var modal_1 = require("app/actionCreators/modal");
var constants_1 = require("app/constants");
var apiErrorCodes_1 = require("app/constants/apiErrorCodes");
var analytics_1 = require("app/utils/analytics");
var apiSentryClient_1 = require("app/utils/apiSentryClient");
var getCsrfToken_1 = tslib_1.__importDefault(require("app/utils/getCsrfToken"));
var guid_1 = require("app/utils/guid");
var createRequestError_1 = tslib_1.__importDefault(require("app/utils/requestError/createRequestError"));
var Request = /** @class */ (function () {
    function Request(requestPromise, aborter) {
        this.requestPromise = requestPromise;
        this.aborter = aborter;
        this.alive = true;
    }
    Request.prototype.cancel = function () {
        var _a;
        this.alive = false;
        (_a = this.aborter) === null || _a === void 0 ? void 0 : _a.abort();
        analytics_1.metric('app.api.request-abort', 1);
    };
    return Request;
}());
exports.Request = Request;
/**
 * Check if the requested method does not require CSRF tokens
 */
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method !== null && method !== void 0 ? method : '');
}
// TODO: Need better way of identifying anonymous pages that don't trigger redirect
var ALLOWED_ANON_PAGES = [
    /^\/accept\//,
    /^\/share\//,
    /^\/auth\/login\//,
    /^\/join-request\//,
];
var globalErrorHandlers = [];
var initApiClientErrorHandling = function () {
    return globalErrorHandlers.push(function (jqXHR) {
        var _a, _b, _c, _d;
        var pageAllowsAnon = ALLOWED_ANON_PAGES.find(function (regex) {
            return regex.test(window.location.pathname);
        });
        // Ignore error unless it is a 401
        if (!jqXHR || jqXHR.status !== 401 || pageAllowsAnon) {
            return;
        }
        var code = (_b = (_a = jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) === null || _b === void 0 ? void 0 : _b.code;
        var extra = (_d = (_c = jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.responseJSON) === null || _c === void 0 ? void 0 : _c.detail) === null || _d === void 0 ? void 0 : _d.extra;
        // 401s can also mean sudo is required or it's a request that is allowed to fail
        // Ignore if these are the cases
        if ([
            'sudo-required',
            'ignore',
            '2fa-required',
            'app-connect-authentication-error',
            'itunes-authentication-error',
            'itunes-2fa-required',
        ].includes(code)) {
            return;
        }
        // If user must login via SSO, redirect to org login page
        if (code === 'sso-required') {
            window.location.assign(extra.loginUrl);
            return;
        }
        if (code === 'member-disabled-over-limit') {
            react_router_1.browserHistory.replace(extra.next);
        }
        // Otherwise, the user has become unauthenticated. Send them to auth
        js_cookie_1.default.set('session_expired', '1');
        if (constants_1.EXPERIMENTAL_SPA) {
            react_router_1.browserHistory.replace('/auth/login/');
        }
        else {
            window.location.reload();
        }
    });
};
exports.initApiClientErrorHandling = initApiClientErrorHandling;
/**
 * Construct a full request URL
 */
function buildRequestUrl(baseUrl, path, query) {
    var params;
    try {
        params = jquery_1.default.param(query !== null && query !== void 0 ? query : [], true);
    }
    catch (err) {
        apiSentryClient_1.run(function (Sentry) {
            return Sentry.withScope(function (scope) {
                scope.setExtra('path', path);
                scope.setExtra('query', query);
                Sentry.captureException(err);
            });
        });
        throw err;
    }
    var fullUrl;
    // Append the baseUrl
    if (path.indexOf(baseUrl) === -1) {
        fullUrl = baseUrl + path;
    }
    else {
        fullUrl = path;
    }
    if (!params) {
        return fullUrl;
    }
    // Append query parameters
    if (fullUrl.indexOf('?') !== -1) {
        fullUrl += '&' + params;
    }
    else {
        fullUrl += '?' + params;
    }
    return fullUrl;
}
/**
 * Check if the API response says project has been renamed.  If so, redirect
 * user to new project slug
 */
// TODO(ts): refine this type later
function hasProjectBeenRenamed(response) {
    var _a, _b, _c, _d, _e;
    var code = (_b = (_a = response === null || response === void 0 ? void 0 : response.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) === null || _b === void 0 ? void 0 : _b.code;
    // XXX(billy): This actually will never happen because we can't intercept the 302
    // jQuery ajax will follow the redirect by default...
    if (code !== apiErrorCodes_1.PROJECT_MOVED) {
        return false;
    }
    var slug = (_e = (_d = (_c = response === null || response === void 0 ? void 0 : response.responseJSON) === null || _c === void 0 ? void 0 : _c.detail) === null || _d === void 0 ? void 0 : _d.extra) === null || _e === void 0 ? void 0 : _e.slug;
    modal_1.redirectToProject(slug);
    return true;
}
exports.hasProjectBeenRenamed = hasProjectBeenRenamed;
/**
 * The API client is used to make HTTP requests to Sentry's backend.
 *
 * This is they preferred way to talk to the backend.
 */
var Client = /** @class */ (function () {
    function Client(options) {
        if (options === void 0) { options = {}; }
        var _a;
        this.baseUrl = (_a = options.baseUrl) !== null && _a !== void 0 ? _a : '/api/0';
        this.activeRequests = {};
    }
    Client.prototype.wrapCallback = function (id, func, cleanup) {
        var _this = this;
        if (cleanup === void 0) { cleanup = false; }
        return function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            var req = _this.activeRequests[id];
            if (cleanup === true) {
                delete _this.activeRequests[id];
            }
            if (req && req.alive) {
                // Check if API response is a 302 -- means project slug was renamed and user
                // needs to be redirected
                // @ts-expect-error
                if (hasProjectBeenRenamed.apply(void 0, tslib_1.__spreadArray([], tslib_1.__read(args)))) {
                    return;
                }
                if (isUndefined_1.default(func)) {
                    return;
                }
                // Call success callback
                return func.apply(req, args); // eslint-disable-line
            }
        };
    };
    /**
     * Attempt to cancel all active XHR requests
     */
    Client.prototype.clear = function () {
        Object.values(this.activeRequests).forEach(function (r) { return r.cancel(); });
    };
    Client.prototype.handleRequestError = function (_a, response, textStatus, errorThrown) {
        var _this = this;
        var _b, _c;
        var id = _a.id, path = _a.path, requestOptions = _a.requestOptions;
        var code = (_c = (_b = response === null || response === void 0 ? void 0 : response.responseJSON) === null || _b === void 0 ? void 0 : _b.detail) === null || _c === void 0 ? void 0 : _c.code;
        var isSudoRequired = code === apiErrorCodes_1.SUDO_REQUIRED || code === apiErrorCodes_1.SUPERUSER_REQUIRED;
        var didSuccessfullyRetry = false;
        if (isSudoRequired) {
            modal_1.openSudo({
                superuser: code === apiErrorCodes_1.SUPERUSER_REQUIRED,
                sudo: code === apiErrorCodes_1.SUDO_REQUIRED,
                retryRequest: function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
                    var data, err_1;
                    var _a, _b;
                    return tslib_1.__generator(this, function (_c) {
                        switch (_c.label) {
                            case 0:
                                _c.trys.push([0, 2, , 3]);
                                return [4 /*yield*/, this.requestPromise(path, requestOptions)];
                            case 1:
                                data = _c.sent();
                                (_a = requestOptions.success) === null || _a === void 0 ? void 0 : _a.call(requestOptions, data);
                                didSuccessfullyRetry = true;
                                return [3 /*break*/, 3];
                            case 2:
                                err_1 = _c.sent();
                                (_b = requestOptions.error) === null || _b === void 0 ? void 0 : _b.call(requestOptions, err_1);
                                return [3 /*break*/, 3];
                            case 3: return [2 /*return*/];
                        }
                    });
                }); },
                onClose: function () { var _a; 
                // If modal was closed, then forward the original response
                return !didSuccessfullyRetry && ((_a = requestOptions.error) === null || _a === void 0 ? void 0 : _a.call(requestOptions, response)); },
            });
            return;
        }
        // Call normal error callback
        var errorCb = this.wrapCallback(id, requestOptions.error);
        errorCb === null || errorCb === void 0 ? void 0 : errorCb(response, textStatus, errorThrown);
    };
    /**
     * Initate a request to the backend API.
     *
     * Consider using `requestPromise` for the async Promise version of this method.
     */
    Client.prototype.request = function (path, options) {
        var _this = this;
        if (options === void 0) { options = {}; }
        var method = options.method || (options.data ? 'POST' : 'GET');
        var fullUrl = buildRequestUrl(this.baseUrl, path, options.query);
        var data = options.data;
        if (!isUndefined_1.default(data) && method !== 'GET') {
            data = JSON.stringify(data);
        }
        // TODO(epurkhiser): Mimicking the old jQuery API, data could be a string /
        // object for GET requets. jQuery just sticks it onto the URL as query
        // parameters
        if (method === 'GET' && data) {
            var queryString = typeof data === 'string' ? data : jquery_1.default.param(data);
            if (queryString.length > 0) {
                fullUrl = fullUrl + (fullUrl.indexOf('?') !== -1 ? '&' : '?') + queryString;
            }
        }
        var id = guid_1.uniqueId();
        var startMarker = "api-request-start-" + id;
        analytics_1.metric.mark({ name: startMarker });
        var errorObject = new Error();
        /**
         * Called when the request completes with a 2xx status
         */
        var successHandler = function (responseData, textStatus, xhr) {
            analytics_1.metric.measure({
                name: 'app.api.request-success',
                start: startMarker,
                data: { status: xhr === null || xhr === void 0 ? void 0 : xhr.status },
            });
            if (!isUndefined_1.default(options.success)) {
                _this.wrapCallback(id, options.success)(responseData, textStatus, xhr);
            }
        };
        /**
         * Called when the request is non-2xx
         */
        var errorHandler = function (resp, textStatus, errorThrown) {
            analytics_1.metric.measure({
                name: 'app.api.request-error',
                start: startMarker,
                data: { status: resp === null || resp === void 0 ? void 0 : resp.status },
            });
            if (resp &&
                resp.status !== 0 &&
                resp.status !== 404 &&
                errorThrown !== 'Request was aborted') {
                apiSentryClient_1.run(function (Sentry) {
                    return Sentry.withScope(function (scope) {
                        var _a;
                        // `requestPromise` can pass its error object
                        var preservedError = (_a = options.preservedError) !== null && _a !== void 0 ? _a : errorObject;
                        var errorObjectToUse = createRequestError_1.default(resp, preservedError.stack, method, path);
                        errorObjectToUse.removeFrames(3);
                        // Setting this to warning because we are going to capture all failed requests
                        scope.setLevel(react_1.Severity.Warning);
                        scope.setTag('http.statusCode', String(resp.status));
                        scope.setTag('error.reason', errorThrown);
                        Sentry.captureException(errorObjectToUse);
                    });
                });
            }
            _this.handleRequestError({ id: id, path: path, requestOptions: options }, resp, textStatus, errorThrown);
        };
        /**
         * Called when the request completes
         */
        var completeHandler = function (jqXHR, textStatus) {
            return _this.wrapCallback(id, options.complete, true)(jqXHR, textStatus);
        };
        // AbortController is optional, though most browser should support it.
        var aborter = typeof AbortController !== 'undefined' ? new AbortController() : undefined;
        // GET requests may not have a body
        var body = method !== 'GET' ? data : undefined;
        var headers = new Headers({
            Accept: 'application/json; charset=utf-8',
            'Content-Type': 'application/json',
        });
        // Do not set the X-CSRFToken header when making a request outside of the
        // current domain
        var absoluteUrl = new URL(fullUrl, window.location.origin);
        var isSameOrigin = window.location.origin === absoluteUrl.origin;
        if (!csrfSafeMethod(method) && isSameOrigin) {
            headers.set('X-CSRFToken', getCsrfToken_1.default());
        }
        var fetchRequest = fetch(fullUrl, {
            method: method,
            body: body,
            headers: headers,
            credentials: 'same-origin',
            signal: aborter === null || aborter === void 0 ? void 0 : aborter.signal,
        });
        // XXX(epurkhiser): We're migrating off of jquery, so for now we have a
        // compatibility layer which mimics that of the jquery response objects.
        fetchRequest
            .then(function (response) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var responseClone, responseJSON, responseText, status, statusText, ok, errorReason, error_1, responseContentType, isResponseJSON, isStatus3XX, error_2, emulatedJQueryXHR, responseData;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        responseClone = response.clone();
                        status = response.status, statusText = response.statusText;
                        ok = response.ok;
                        errorReason = 'Request not OK';
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, response.text()];
                    case 2:
                        responseText = _a.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _a.sent();
                        ok = false;
                        if (error_1.name === 'AbortError') {
                            errorReason = 'Request was aborted';
                        }
                        else {
                            errorReason = error_1.toString();
                        }
                        return [3 /*break*/, 4];
                    case 4:
                        responseContentType = response.headers.get('content-type');
                        isResponseJSON = responseContentType === null || responseContentType === void 0 ? void 0 : responseContentType.includes('json');
                        isStatus3XX = status >= 300 && status < 400;
                        if (!(status !== 204 && !isStatus3XX)) return [3 /*break*/, 8];
                        _a.label = 5;
                    case 5:
                        _a.trys.push([5, 7, , 8]);
                        return [4 /*yield*/, responseClone.json()];
                    case 6:
                        responseJSON = _a.sent();
                        return [3 /*break*/, 8];
                    case 7:
                        error_2 = _a.sent();
                        if (error_2.name === 'AbortError') {
                            ok = false;
                            errorReason = 'Request was aborted';
                        }
                        else if (isResponseJSON && error_2 instanceof SyntaxError) {
                            // If the MIME type is `application/json` but decoding failed,
                            // this should be an error.
                            ok = false;
                            errorReason = 'JSON parse error';
                        }
                        return [3 /*break*/, 8];
                    case 8:
                        emulatedJQueryXHR = {
                            status: status,
                            statusText: statusText,
                            responseJSON: responseJSON,
                            responseText: responseText,
                            getResponseHeader: function (header) { return response.headers.get(header); },
                        };
                        responseData = isResponseJSON ? responseJSON : responseText;
                        if (ok) {
                            successHandler(responseData, statusText, emulatedJQueryXHR);
                        }
                        else {
                            globalErrorHandlers.forEach(function (handler) { return handler(emulatedJQueryXHR); });
                            errorHandler(emulatedJQueryXHR, statusText, errorReason);
                        }
                        completeHandler(emulatedJQueryXHR, statusText);
                        return [2 /*return*/];
                }
            });
        }); })
            .catch(function (err) {
            // Aborts are expected
            if ((err === null || err === void 0 ? void 0 : err.name) === 'AbortError') {
                return;
            }
            // The request failed for other reason
            apiSentryClient_1.run(function (Sentry) {
                return Sentry.withScope(function (scope) {
                    scope.setLevel(react_1.Severity.Warning);
                    Sentry.captureException(err);
                });
            });
        });
        var request = new Request(fetchRequest, aborter);
        this.activeRequests[id] = request;
        return request;
    };
    Client.prototype.requestPromise = function (path, _a) {
        var _this = this;
        if (_a === void 0) { _a = {}; }
        var includeAllArgs = _a.includeAllArgs, options = tslib_1.__rest(_a, ["includeAllArgs"]);
        // Create an error object here before we make any async calls so
        // that we have a helpful stack trace if it errors
        //
        // This *should* get logged to Sentry only if the promise rejection is not handled
        // (since SDK captures unhandled rejections). Ideally we explicitly ignore rejection
        // or handle with a user friendly error message
        var preservedError = new Error();
        return new Promise(function (resolve, reject) {
            _this.request(path, tslib_1.__assign(tslib_1.__assign({}, options), { preservedError: preservedError, success: function (data, textStatus, xhr) {
                    includeAllArgs ? resolve([data, textStatus, xhr]) : resolve(data);
                }, error: function (resp) {
                    var errorObjectToUse = createRequestError_1.default(resp, preservedError.stack, options.method, path);
                    errorObjectToUse.removeFrames(2);
                    // Although `this.request` logs all error responses, this error object can
                    // potentially be logged by Sentry's unhandled rejection handler
                    reject(errorObjectToUse);
                } }));
        });
    };
    return Client;
}());
exports.Client = Client;
//# sourceMappingURL=api.jsx.map