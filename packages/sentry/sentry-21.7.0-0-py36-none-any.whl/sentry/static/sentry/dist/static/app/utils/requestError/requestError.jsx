Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var RequestError = /** @class */ (function (_super) {
    tslib_1.__extends(RequestError, _super);
    function RequestError(method, path) {
        var _newTarget = this.constructor;
        var _this = _super.call(this, (method || 'GET') + " " + path) || this;
        _this.name = 'RequestError';
        Object.setPrototypeOf(_this, _newTarget.prototype);
        return _this;
    }
    /**
     * Updates Error with XHR response
     */
    RequestError.prototype.setResponse = function (resp) {
        if (resp) {
            this.setMessage(this.message + " " + (typeof resp.status === 'number' ? resp.status : 'n/a'));
            // Some callback handlers expect these properties on the error object
            if (resp.responseText) {
                this.responseText = resp.responseText;
            }
            if (resp.responseJSON) {
                this.responseJSON = resp.responseJSON;
            }
            this.status = resp.status;
            this.statusText = resp.statusText;
        }
    };
    RequestError.prototype.setMessage = function (message) {
        this.message = message;
    };
    RequestError.prototype.setStack = function (newStack) {
        this.stack = newStack;
    };
    RequestError.prototype.setName = function (name) {
        this.name = name;
    };
    RequestError.prototype.removeFrames = function (numLinesToRemove) {
        // Drop some frames so stack trace starts at callsite
        //
        // Note that babel will add a call to support extending Error object
        // Old browsers may not have stack trace
        if (!this.stack) {
            return;
        }
        var lines = this.stack.split('\n');
        this.stack = tslib_1.__spreadArray([lines[0]], tslib_1.__read(lines.slice(numLinesToRemove))).join('\n');
    };
    return RequestError;
}(Error));
exports.default = RequestError;
//# sourceMappingURL=requestError.jsx.map