#!/bin/bash
curl -sfL https://get.k3s.io | sh -
systemctl enable k3s
systemctl start k3s
