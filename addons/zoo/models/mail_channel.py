from odoo import models, api

class MailChannel(models.Model):
    _inherit = 'mail.channel'

    # Thêm field để phân biệt kênh chat support
    is_customer_support = fields.Boolean(default=False)

    # Hàm 1: Lấy lịch sử chat
    def mobile_chat_channel_fetch_message(self, channel_id, last_id=False, limit=20):
        channel_id = int(channel_id)
        last_id = int(last_id) if last_id else last_id
        limit = int(limit)
        
        if channel_id > 0:
            # Có channel_id → lấy lịch sử chat của channel đó
            return self.env["mail.channel"].browse(channel_id)\
                .channel_fetch_message(last_id=last_id, limit=limit)
        else:
            # Chưa có channel → trả về rỗng
            return []

    # Hàm 2: Gửi tin nhắn
    def mobile_chat_message_post(self, channel_id, body):
        channel_id = int(channel_id)
        
        if channel_id == 0:
            # Chưa có channel_id → tìm hoặc tạo mới
            q_channel_id = self._get_channel_id()
            
            if not q_channel_id:
                # Chưa từng chat → tạo kênh mới
                customer_partner = self.env.user.partner_id
                target_mail_channel = self.env["mail.channel"].create({
                    "name": "%s (Customer Support)" % customer_partner.name,
                    "channel_partner_ids": [(6, 0, [customer_partner.id] + self._get_admin_partner_ids())],
                    "channel_type": "channel",
                    "public": "private",
                    "is_customer_support": True,
                })
            else:
                target_mail_channel = self.env["mail.channel"].browse(q_channel_id)
        else:
            target_mail_channel = self.env["mail.channel"].browse(channel_id)

        if target_mail_channel:
            message = target_mail_channel.message_post(
                body=body,
                message_type="comment",
                subtype_xmlid="mail.mt_comment"
            )
            return {
                "channel_id": target_mail_channel.id,
                "id": message.id,
                "message": self.mobile_chat_channel_fetch_message(
                    channel_id=target_mail_channel.id, last_id=False, limit=1
                )[0],
            } if message else {"error": "Failed to send message!"}
        else:
            return {"error": "No channel found!"}

    # Hàm 3: Tìm channel_id của user hiện tại
    def _get_channel_id(self):
        customer_partner = self.env.user.partner_id
        mail_channel = self.env["mail.channel"].search([
            ("channel_type", "=", "channel"),
            ("channel_partner_ids", "in", [customer_partner.id]),
            ("public", "=", "private"),
            ("is_customer_support", "=", True),
        ], limit=1)
        return mail_channel.id if mail_channel else False

    # Hàm 4: Lấy danh sách partner của admin
    def _get_admin_partner_ids(self):
        admin_ids = []
        
        # Ưu tiên lấy từ group super admin (nếu có module b2x_perm)
        b2x_super_admin_group = self.env.ref(
            "b2x_perm.group_b2x_super_admin", raise_if_not_found=False
        )
        if b2x_super_admin_group:
            super_admin_users = b2x_super_admin_group.sudo()\
                .with_context(active_test=False).mapped("users")
            admin_ids += [u.partner_id.id for u in super_admin_users]
        
        # Không có group → dùng admin mặc định
        if not admin_ids:
            admin_partner = self.env.ref("base.user_admin").partner_id
            admin_ids.append(admin_partner.id)
        
        return admin_ids