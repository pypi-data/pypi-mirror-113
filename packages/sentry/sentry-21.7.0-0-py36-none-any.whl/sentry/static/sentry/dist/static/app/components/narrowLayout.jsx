Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var account_1 = require("app/actionCreators/account");
var api_1 = require("app/api");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var NarrowLayout = /** @class */ (function (_super) {
    tslib_1.__extends(NarrowLayout, _super);
    function NarrowLayout() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.api = new api_1.Client();
        _this.handleLogout = function () {
            account_1.logout(_this.api).then(function () { return window.location.assign('/auth/login'); });
        };
        return _this;
    }
    NarrowLayout.prototype.UNSAFE_componentWillMount = function () {
        document.body.classList.add('narrow');
    };
    NarrowLayout.prototype.componentWillUnmount = function () {
        this.api.clear();
        document.body.classList.remove('narrow');
    };
    NarrowLayout.prototype.render = function () {
        return (<div className="app">
        <div className="pattern-bg"/>
        <div className="container" style={{ maxWidth: this.props.maxWidth }}>
          <div className="box box-modal">
            <div className="box-header">
              <a href="/">
                <icons_1.IconSentry size="lg"/>
              </a>
              {this.props.showLogout && (<a className="logout pull-right" onClick={this.handleLogout}>
                  <Logout>{locale_1.t('Sign out')}</Logout>
                </a>)}
            </div>
            <div className="box-content with-padding">{this.props.children}</div>
          </div>
        </div>
      </div>);
    };
    return NarrowLayout;
}(react_1.Component));
var Logout = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: 16px;\n"], ["\n  font-size: 16px;\n"])));
exports.default = NarrowLayout;
var templateObject_1;
//# sourceMappingURL=narrowLayout.jsx.map