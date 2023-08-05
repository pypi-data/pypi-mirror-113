Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var forms_1 = require("app/components/forms");
var internalStatChart_1 = tslib_1.__importDefault(require("app/components/internalStatChart"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var AdminQuotas = /** @class */ (function (_super) {
    tslib_1.__extends(AdminQuotas, _super);
    function AdminQuotas() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AdminQuotas.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { since: new Date().getTime() / 1000 - 3600 * 24 * 7, resolution: '1h' });
    };
    AdminQuotas.prototype.getEndpoints = function () {
        return [['config', '/internal/quotas/']];
    };
    AdminQuotas.prototype.renderBody = function () {
        var config = this.state.config;
        return (<div>
        <h3>Quotas</h3>

        <div className="box">
          <div className="box-header">
            <h4>Config</h4>
          </div>

          <div className="box-content with-padding">
            <forms_1.TextField name="backend" value={config.backend} label="Backend" disabled/>
            <forms_1.TextField name="rateLimit" value={config.options['system.rate-limit']} label="Rate Limit" disabled/>
          </div>
        </div>

        <div className="box">
          <div className="box-header">
            <h4>Total Events</h4>
          </div>
          <internalStatChart_1.default since={this.state.since} resolution={this.state.resolution} stat="events.total" label="Events"/>
        </div>

        <div className="box">
          <div className="box-header">
            <h4>Dropped Events</h4>
          </div>
          <internalStatChart_1.default since={this.state.since} resolution={this.state.resolution} stat="events.dropped" label="Events"/>
        </div>
      </div>);
    };
    return AdminQuotas;
}(asyncView_1.default));
exports.default = AdminQuotas;
//# sourceMappingURL=adminQuotas.jsx.map