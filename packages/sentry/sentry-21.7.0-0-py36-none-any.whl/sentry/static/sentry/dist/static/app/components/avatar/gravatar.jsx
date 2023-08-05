Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var qs = tslib_1.__importStar(require("query-string"));
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var callIfFunction_1 = require("app/utils/callIfFunction");
var styles_1 = require("./styles");
var Gravatar = /** @class */ (function (_super) {
    tslib_1.__extends(Gravatar, _super);
    function Gravatar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            MD5: undefined,
        };
        _this._isMounted = false;
        _this.buildGravatarUrl = function () {
            var _a = _this.props, gravatarId = _a.gravatarId, remoteSize = _a.remoteSize, placeholder = _a.placeholder;
            var url = configStore_1.default.getConfig().gravatarBaseUrl + '/avatar/';
            var md5 = callIfFunction_1.callIfFunction(_this.state.MD5, gravatarId);
            if (md5) {
                url += md5;
            }
            var query = {
                s: remoteSize || undefined,
                // If gravatar is not found we need the request to return an error,
                // otherwise error handler will not trigger and avatar will not have a display a LetterAvatar backup.
                d: placeholder || '404',
            };
            url += '?' + qs.stringify(query);
            return url;
        };
        return _this;
    }
    Gravatar.prototype.componentDidMount = function () {
        var _this = this;
        this._isMounted = true;
        Promise.resolve().then(function () { return tslib_1.__importStar(require('crypto-js/md5')); }).then(function (mod) { return mod.default; })
            .then(function (MD5) {
            if (!_this._isMounted) {
                return;
            }
            _this.setState({ MD5: MD5 });
        });
    };
    Gravatar.prototype.componentWillUnmount = function () {
        // Need to track mounted state because `React.isMounted()` is deprecated and because of
        // dynamic imports
        this._isMounted = false;
    };
    Gravatar.prototype.render = function () {
        if (!this.state.MD5) {
            return null;
        }
        var _a = this.props, round = _a.round, onError = _a.onError, onLoad = _a.onLoad, suggested = _a.suggested, grayscale = _a.grayscale;
        return (<Image round={round} src={this.buildGravatarUrl()} onLoad={onLoad} onError={onError} suggested={suggested} grayscale={grayscale}/>);
    };
    return Gravatar;
}(react_1.Component));
exports.default = Gravatar;
var Image = styled_1.default('img')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), styles_1.imageStyle);
var templateObject_1;
//# sourceMappingURL=gravatar.jsx.map