Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var isFunction_1 = tslib_1.__importDefault(require("lodash/isFunction"));
var indicator_1 = require("app/actionCreators/indicator");
var api_1 = require("app/api");
var forms_1 = require("app/components/forms");
var locale_1 = require("app/locale");
var callbackWithArgs = function (context, callback) {
    var args = [];
    for (var _i = 2; _i < arguments.length; _i++) {
        args[_i - 2] = arguments[_i];
    }
    return isFunction_1.default(callback) ? callback.bind.apply(callback, tslib_1.__spreadArray([context], tslib_1.__read(args))) : undefined;
};
var PluginComponentBase = /** @class */ (function (_super) {
    tslib_1.__extends(PluginComponentBase, _super);
    function PluginComponentBase(props, context) {
        var _this = _super.call(this, props, context) || this;
        _this.api = new api_1.Client();
        [
            'onLoadSuccess',
            'onLoadError',
            'onSave',
            'onSaveSuccess',
            'onSaveError',
            'onSaveComplete',
            'renderField',
        ].map(function (method) { return (_this[method] = _this[method].bind(_this)); });
        if (_this.fetchData) {
            _this.fetchData = _this.onLoad.bind(_this, _this.fetchData.bind(_this));
        }
        if (_this.onSubmit) {
            _this.onSubmit = _this.onSave.bind(_this, _this.onSubmit.bind(_this));
        }
        _this.state = {
            state: forms_1.FormState.READY,
        };
        return _this;
    }
    PluginComponentBase.prototype.componentWillUnmount = function () {
        this.api.clear();
    };
    PluginComponentBase.prototype.fetchData = function () {
        // Allow children to implement this
    };
    PluginComponentBase.prototype.onSubmit = function () {
        // Allow children to implement this
    };
    PluginComponentBase.prototype.onLoad = function (callback) {
        var args = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            args[_i - 1] = arguments[_i];
        }
        this.setState({
            state: forms_1.FormState.LOADING,
        }, callbackWithArgs.apply(void 0, tslib_1.__spreadArray([this, callback], tslib_1.__read(args))));
    };
    PluginComponentBase.prototype.onLoadSuccess = function () {
        this.setState({
            state: forms_1.FormState.READY,
        });
    };
    PluginComponentBase.prototype.onLoadError = function (callback) {
        var args = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            args[_i - 1] = arguments[_i];
        }
        this.setState({
            state: forms_1.FormState.ERROR,
        }, callbackWithArgs.apply(void 0, tslib_1.__spreadArray([this, callback], tslib_1.__read(args))));
        indicator_1.addErrorMessage(locale_1.t('An error occurred.'));
    };
    PluginComponentBase.prototype.onSave = function (callback) {
        var args = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            args[_i - 1] = arguments[_i];
        }
        if (this.state.state === forms_1.FormState.SAVING) {
            return;
        }
        callback = callbackWithArgs.apply(void 0, tslib_1.__spreadArray([this, callback], tslib_1.__read(args)));
        this.setState({
            state: forms_1.FormState.SAVING,
        }, function () {
            indicator_1.addLoadingMessage(locale_1.t('Saving changes\u2026'));
            callback && callback();
        });
    };
    PluginComponentBase.prototype.onSaveSuccess = function (callback) {
        var args = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            args[_i - 1] = arguments[_i];
        }
        callback = callbackWithArgs.apply(void 0, tslib_1.__spreadArray([this, callback], tslib_1.__read(args)));
        this.setState({
            state: forms_1.FormState.READY,
        }, function () { return callback && callback(); });
        setTimeout(function () {
            indicator_1.addSuccessMessage(locale_1.t('Success!'));
        }, 0);
    };
    PluginComponentBase.prototype.onSaveError = function (callback) {
        var args = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            args[_i - 1] = arguments[_i];
        }
        callback = callbackWithArgs.apply(void 0, tslib_1.__spreadArray([this, callback], tslib_1.__read(args)));
        this.setState({
            state: forms_1.FormState.ERROR,
        }, function () { return callback && callback(); });
        setTimeout(function () {
            indicator_1.addErrorMessage(locale_1.t('Unable to save changes. Please try again.'));
        }, 0);
    };
    PluginComponentBase.prototype.onSaveComplete = function (callback) {
        var args = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            args[_i - 1] = arguments[_i];
        }
        indicator_1.clearIndicators();
        callback = callbackWithArgs.apply(void 0, tslib_1.__spreadArray([this, callback], tslib_1.__read(args)));
        callback && callback();
    };
    PluginComponentBase.prototype.renderField = function (props) {
        var _a;
        props = tslib_1.__assign({}, props);
        var newProps = tslib_1.__assign(tslib_1.__assign({}, props), { formState: this.state.state });
        return <forms_1.GenericField key={(_a = newProps.config) === null || _a === void 0 ? void 0 : _a.name} {...newProps}/>;
    };
    return PluginComponentBase;
}(React.Component));
exports.default = PluginComponentBase;
//# sourceMappingURL=pluginComponentBase.jsx.map