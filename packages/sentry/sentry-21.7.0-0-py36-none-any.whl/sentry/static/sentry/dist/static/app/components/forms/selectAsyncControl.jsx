Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var debounce_1 = tslib_1.__importDefault(require("lodash/debounce"));
var indicator_1 = require("app/actionCreators/indicator");
var api_1 = require("app/api");
var locale_1 = require("app/locale");
var handleXhrErrorResponse_1 = tslib_1.__importDefault(require("app/utils/handleXhrErrorResponse"));
var selectControl_1 = tslib_1.__importDefault(require("./selectControl"));
/**
 * Performs an API request to `url` when menu is initially opened
 */
var SelectAsyncControl = /** @class */ (function (_super) {
    tslib_1.__extends(SelectAsyncControl, _super);
    function SelectAsyncControl(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {};
        _this.doQuery = debounce_1.default(function (cb) {
            var _a = _this.props, url = _a.url, onQuery = _a.onQuery;
            var query = _this.state.query;
            if (!_this.api) {
                return null;
            }
            return _this.api
                .requestPromise(url, {
                query: typeof onQuery === 'function' ? onQuery(query) : { query: query },
            })
                .then(function (data) { return cb(null, data); }, function (err) { return cb(err); });
        }, 250);
        _this.handleLoadOptions = function () {
            return new Promise(function (resolve, reject) {
                _this.doQuery(function (err, result) {
                    if (err) {
                        reject(err);
                    }
                    else {
                        resolve(result);
                    }
                });
            }).then(function (resp) {
                var onResults = _this.props.onResults;
                return typeof onResults === 'function' ? onResults(resp) : resp;
            }, function (err) {
                indicator_1.addErrorMessage(locale_1.t('There was a problem with the request.'));
                handleXhrErrorResponse_1.default('SelectAsync failed')(err);
                // eslint-disable-next-line no-console
                console.error(err);
            });
        };
        _this.handleInputChange = function (query) {
            _this.setState({ query: query });
        };
        _this.api = new api_1.Client();
        _this.state = {
            query: '',
        };
        _this.cache = {};
        return _this;
    }
    SelectAsyncControl.prototype.componentWillUnmount = function () {
        if (!this.api) {
            return;
        }
        this.api.clear();
        this.api = null;
    };
    SelectAsyncControl.prototype.render = function () {
        var _a = this.props, value = _a.value, forwardedRef = _a.forwardedRef, props = tslib_1.__rest(_a, ["value", "forwardedRef"]);
        return (<selectControl_1.default 
        // The key is used as a way to force a reload of the options:
        // https://github.com/JedWatson/react-select/issues/1879#issuecomment-316871520
        key={value} ref={forwardedRef} value={value} defaultOptions loadOptions={this.handleLoadOptions} onInputChange={this.handleInputChange} async cache={this.cache} {...props}/>);
    };
    SelectAsyncControl.defaultProps = {
        placeholder: '--',
    };
    return SelectAsyncControl;
}(React.Component));
var forwardRef = function (p, ref) { return <SelectAsyncControl {...p} forwardedRef={ref}/>; };
forwardRef.displayName = 'SelectAsyncControl';
exports.default = React.forwardRef(forwardRef);
//# sourceMappingURL=selectAsyncControl.jsx.map