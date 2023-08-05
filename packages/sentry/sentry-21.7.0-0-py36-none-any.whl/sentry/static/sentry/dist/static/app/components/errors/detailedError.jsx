Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
function openFeedback(e) {
    e.preventDefault();
    Sentry.showReportDialog();
}
var DetailedError = /** @class */ (function (_super) {
    tslib_1.__extends(DetailedError, _super);
    function DetailedError() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DetailedError.prototype.componentDidMount = function () {
        var _this = this;
        // XXX(epurkhiser): Why is this here?
        setTimeout(function () { return _this.forceUpdate(); }, 100);
    };
    DetailedError.prototype.render = function () {
        var _a = this.props, className = _a.className, heading = _a.heading, message = _a.message, onRetry = _a.onRetry, hideSupportLinks = _a.hideSupportLinks;
        var cx = classnames_1.default('detailed-error', className);
        var showFooter = !!onRetry || !hideSupportLinks;
        return (<div className={cx}>
        <div className="detailed-error-icon">
          <icons_1.IconFlag size="lg"/>
        </div>
        <div className="detailed-error-content">
          <h4>{heading}</h4>

          <div className="detailed-error-content-body">{message}</div>

          {showFooter && (<div className="detailed-error-content-footer">
              <div>
                {onRetry && (<a onClick={onRetry} className="btn btn-default">
                    {locale_1.t('Retry')}
                  </a>)}
              </div>

              {!hideSupportLinks && (<div className="detailed-error-support-links">
                  {Sentry.lastEventId() && (<button_1.default priority="link" onClick={openFeedback}>
                      {locale_1.t('Fill out a report')}
                    </button_1.default>)}
                  <a href="https://status.sentry.io/">{locale_1.t('Service status')}</a>

                  <a href="https://sentry.io/support/">{locale_1.t('Contact support')}</a>
                </div>)}
            </div>)}
        </div>
      </div>);
    };
    DetailedError.defaultProps = {
        hideSupportLinks: false,
    };
    return DetailedError;
}(React.Component));
exports.default = DetailedError;
//# sourceMappingURL=detailedError.jsx.map