Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var locale_1 = require("app/locale");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var SetupWizard = /** @class */ (function (_super) {
    tslib_1.__extends(SetupWizard, _super);
    function SetupWizard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            finished: false,
        };
        return _this;
    }
    SetupWizard.prototype.UNSAFE_componentWillMount = function () {
        this.pollFinished();
    };
    SetupWizard.prototype.pollFinished = function () {
        var _this = this;
        return new Promise(function (resolve) {
            _this.props.api.request("/wizard/" + _this.props.hash + "/", {
                method: 'GET',
                success: function () {
                    setTimeout(function () { return _this.pollFinished(); }, 1000);
                },
                error: function () {
                    resolve();
                    _this.setState({ finished: true });
                    setTimeout(function () { return window.close(); }, 10000);
                },
            });
        });
    };
    SetupWizard.prototype.renderSuccess = function () {
        return (<div className="row">
        <h5>{locale_1.t('Return to your terminal to complete your setup')}</h5>
        <h5>{locale_1.t('(This window will close in 10 seconds)')}</h5>
        <button className="btn btn-default" onClick={function () { return window.close(); }}>
          Close browser tab
        </button>
      </div>);
    };
    SetupWizard.prototype.renderLoading = function () {
        return (<div className="row">
        <h5>{locale_1.t('Waiting for wizard to connect')}</h5>
      </div>);
    };
    SetupWizard.prototype.render = function () {
        var finished = this.state.finished;
        return (<div className="container">
        <loadingIndicator_1.default style={{ margin: '2em auto' }} finished={finished}>
          {finished ? this.renderSuccess() : this.renderLoading()}
        </loadingIndicator_1.default>
      </div>);
    };
    SetupWizard.defaultProps = {
        hash: false,
    };
    return SetupWizard;
}(react_1.Component));
exports.default = withApi_1.default(SetupWizard);
//# sourceMappingURL=index.jsx.map