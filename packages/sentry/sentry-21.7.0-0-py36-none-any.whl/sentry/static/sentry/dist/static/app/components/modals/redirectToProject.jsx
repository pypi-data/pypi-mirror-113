Object.defineProperty(exports, "__esModule", { value: true });
exports.RedirectToProjectModal = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var ReactRouter = tslib_1.__importStar(require("react-router"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var text_1 = tslib_1.__importDefault(require("app/components/text"));
var locale_1 = require("app/locale");
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var RedirectToProjectModal = /** @class */ (function (_super) {
    tslib_1.__extends(RedirectToProjectModal, _super);
    function RedirectToProjectModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            timer: 5,
        };
        return _this;
    }
    RedirectToProjectModal.prototype.componentDidMount = function () {
        var _this = this;
        setInterval(function () {
            if (_this.state.timer <= 1) {
                window.location.assign(_this.newPath);
                return;
            }
            _this.setState(function (state) { return ({
                timer: state.timer - 1,
            }); });
        }, 1000);
    };
    Object.defineProperty(RedirectToProjectModal.prototype, "newPath", {
        get: function () {
            var _a = this.props, params = _a.params, slug = _a.slug;
            return recreateRoute_1.default('', tslib_1.__assign(tslib_1.__assign({}, this.props), { params: tslib_1.__assign(tslib_1.__assign({}, params), { projectId: slug }) }));
        },
        enumerable: false,
        configurable: true
    });
    RedirectToProjectModal.prototype.render = function () {
        var _a = this.props, slug = _a.slug, Header = _a.Header, Body = _a.Body;
        return (<react_1.Fragment>
        <Header>{locale_1.t('Redirecting to New Project...')}</Header>

        <Body>
          <div>
            <text_1.default>
              <p>{locale_1.t('The project slug has been changed.')}</p>

              <p>
                {locale_1.tct('You will be redirected to the new project [project] in [timer] seconds...', {
                project: <strong>{slug}</strong>,
                timer: "" + this.state.timer,
            })}
              </p>
              <ButtonWrapper>
                <button_1.default priority="primary" href={this.newPath}>
                  {locale_1.t('Continue to %s', slug)}
                </button_1.default>
              </ButtonWrapper>
            </text_1.default>
          </div>
        </Body>
      </react_1.Fragment>);
    };
    return RedirectToProjectModal;
}(react_1.Component));
exports.RedirectToProjectModal = RedirectToProjectModal;
exports.default = ReactRouter.withRouter(RedirectToProjectModal);
var ButtonWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n"])));
var templateObject_1;
//# sourceMappingURL=redirectToProject.jsx.map